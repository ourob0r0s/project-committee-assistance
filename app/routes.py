from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import studentLoginForm, facultyLoginForm, facultyRegisterForm, studentRegisterForm, proposalAdd, groupAdd, groupJoin, deadlineSet, evaluateForm
from app.models import User, Proposal, Group
from app.decorators import isFaculty, isAdmin, isStudent, isLeader
from sqlalchemy.orm import sessionmaker
from array import *
import csv
from datetime import date, timedelta

global dateProposal 
global dateRank 
dateProposal = 'not decided yet'
dateRank = 'not decided yet'

@app.route('/')
@app.route('/index')
def index():
    global dateProposal
    global dateRank
    return render_template("index.html", title='Home Page', dateProposal = dateProposal, dateRank = dateRank)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for("loginChoice"))
@app.route('/login_choice', methods=['GET', 'POST'])
def loginChoice():
    return render_template("auth/login_choice.html",title="login choice")


@app.route('/register_choice', methods=['GET', 'POST'])
def registerChoice():
    return render_template("auth/register_choice.html",title="register choice")
    

@app.route('/student_login', methods=['GET', 'POST'])
def studentLogin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = studentLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(sId=form.sId.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect id or password','danger')
            return redirect(url_for('studentLogin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/student_login.html', title='Sign In', form=form)

@app.route('/faculty_login', methods=['GET', 'POST'])
def facultyLogin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = facultyLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect email or password','danger')
            return redirect(url_for('facultyLogin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/faculty_login.html', title='Sign In', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/student_register', methods=['GET', 'POST'])
def studentRegister():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = studentRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=(str(form.sId.data)+"@student.ksu.edu.sa"), sId=form.sId.data, gpa=form.gpa.data, student = True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!','success')
        return redirect(url_for('studentLogin'))
    return render_template('auth/student_register.html', title='Register', form=form)


@app.route('/faculty_register', methods=['GET', 'POST'])
def facultyRegister():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = facultyRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, faculty = True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!','success')
        return redirect(url_for('facultyLogin'))
    return render_template('auth/faculty_register.html', title='Register', form=form)


@app.route('/deadline', methods=['GET', 'POST'])
@login_required
@isAdmin()
def deadline():
    form = deadlineSet()
    if form.validate_on_submit():
        global dateProposal
        global dateRank
        dateProposal = form.dateProposal.data
        dateRank = form.dateRank.data
        flash('deadline has been submitted!','success')
        return redirect(url_for('index'))
                
    return render_template("deadline.html", title='deadline', form=form)

@app.route('/proposal', methods=['GET', 'POST'])
@login_required
@isFaculty()
def proposal():

    proposals = Proposal.query.filter_by(author = current_user.id)
    
    return render_template("proposal.html", title='Proposal', proposals=proposals)

@app.route('/view_proposal', methods=['GET', 'POST'])
@login_required
@isStudent()
def viewProposal():
    authors = []
    proposals = Proposal.query.filter_by(published = True)
    for proposal in proposals:
        user = User.query.filter_by(id = proposal.author).first()
        authors.append(user.username)
    authors.reverse()
        
        
    return render_template("view_proposal.html", title='Proposal', proposals=proposals, authors = authors)


@app.route('/add_proposal', methods=['GET', 'POST'])
@login_required
@isFaculty()
def addProposal():
    form = proposalAdd()
    if not isinstance(dateProposal, str):
        if dateProposal < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('proposal'))

    count = Proposal.query.filter_by(author = current_user.id).count()
    if count > 1:
        flash('cant add more than 2 proposals!','danger')
        return redirect(url_for('proposal'))
    if form.validate_on_submit():
        prop = Proposal(title= form.title.data, desc=form.desc.data)
        db.session.add(prop)
        db.session.commit()
        prop = Proposal.query.filter_by(title = form.title.data).first()
        props = current_user.author
        props.append(prop)
        current_user.set_author(props)
        flash('Congratulations, your proposal has been added!','success')
        return redirect(url_for('proposal'))
    return render_template("add_proposal.html", title='add Proposal', form=form)



@app.route('/proposal/delete/<int:id>')
@login_required
@isFaculty()
def deleteProposal(id):
    if not isinstance(dateProposal, str):
        if dateProposal < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('proposal'))
    proposal = Proposal.query.get_or_404(id)
    if proposal.published:
            flash('proposal already published!','danger')
            return redirect(url_for('proposal'))
    id = current_user.id
    if id == proposal.author:
        try:
            db.session.delete(proposal)
            db.session.commit()

            # Return a message
            flash("proposal Was Deleted!",'info')

            return redirect(url_for('proposal'))


        except:
            # Return an error message
            flash("Whoops! There was a problem deleting proposal, try again...", 'danger')

            return redirect(url_for('proposal'))
    else:
        # Return a message
        flash("You Aren't Authorized To Delete That Proposal!", 'danger')

        return redirect(url_for('proposal'))



@app.route('/group', methods=['GET', 'POST'])
@login_required
@isStudent()
def group():
    if current_user.member is None:
        return redirect(url_for('joinGroup'))
    group = Group.query.filter_by(id = current_user.member).first()
    members = group.members
    return render_template("group.html", title='Group', group = group)

@app.route('/join_group', methods=['GET', 'POST'])
@login_required
@isStudent()
def joinGroup():
    if current_user.member is not None:
        return redirect(url_for('group'))
    
    form = groupJoin()
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('group'))
    if form.validate_on_submit():
        group = Group.query.filter_by(name = form.name.data).first()
        if group.ranked:
            flash("you cant join a group that already submitted",'danger')
            return redirect(url_for('group'))

        members = group.members
        if len(members) > 2:
            flash('group full!','danger')
            return redirect(url_for('group'))
        members.append(current_user)
        group.set_member(members)
        return redirect(url_for('group'))
    return render_template("join_group.html", title='Join group', form=form)



@app.route('/add_group', methods=['GET', 'POST'])
@login_required
@isStudent()
def addGroup():
    if current_user.member is not None:
        return redirect(url_for('group'))
    form = groupAdd()
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('group'))
    if form.validate_on_submit():
        group = Group(name=form.name.data , score = -1)
        db.session.add(group)
        current_user.leader = True
        db.session.commit()

        group = Group.query.filter_by(name = form.name.data).first()
        members = group.members
        members.append(current_user)
        group.set_member(members)
        

        flash('Congratulations, you have created a group!', 'success')
        return redirect(url_for('group'))
    return render_template("add_group.html", title='Create group', form=form)


@app.route('/group/delete/<int:id>')
@login_required
@isStudent()
@isLeader()
def deleteGroup(id):
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('group'))
    group = Group.query.get_or_404(id)
    if group.ranked:
            flash("you cant delete a group that already submitted",'danger')
            return redirect(url_for('group'))
    try:
        db.session.delete(group)
        current_user.leader = False
        db.session.commit()

        # Return a message
        flash("Group Deleted!",'info')

        return redirect(url_for('joinGroup'))


    except:
        # Return an error message
        flash("Whoops! There was a problem deleting group, try again...", 'danger')

        return redirect(url_for('group'))


@app.route('/group/leave/<int:id>')
@login_required
@isStudent()
def leaveGroup(id):
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('group'))
    if current_user.id == id:
        user = User.query.get_or_404(id)
        group = Group.query.filter_by(id = user.member).first()
        if group.ranked:
            flash("you cant leave a group that already submitted",'danger')
            return redirect(url_for('group'))
        try:
            user.member = None
            db.session.commit()

            # Return a message
            flash("you left the group!",'info')


            return redirect(url_for('group'))

        except:
            # Return an error message
            flash("Whoops! There was a problem, try again...", 'danger')

            return redirect(url_for('group'))
    else:
            # Return an error message
        flash("Whoops! There was a problem, try again...", 'danger')

        return redirect(url_for('group'))

@app.route('/group/remove/<int:id>')
@login_required
@isStudent()
@isLeader()
def removeMember(id):
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('group'))
    if current_user.id != id:
        user = User.query.get_or_404(id)
        group = Group.query.filter_by(id = user.member).first()
        if group.ranked:
                flash("you cant remove a member if you already submitted",'danger')
                return redirect(url_for('group'))
        try:
            user.member = None
            db.session.commit()

            # Return a message
            flash("user was removed!",'info')


            return redirect(url_for('group'))

        except:
            # Return an error message
            flash("Whoops! There was a problem removing member, try again...", 'danger')

            return redirect(url_for('group'))
    else:
            # Return an error message
        flash("Whoops! There was a problem removing member, try again...", 'danger')

        return redirect(url_for('group'))

@app.route('/publish_proposal', methods=['GET', 'POST'])
@login_required
@isAdmin()
def publishProposal():
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('index'))
    proposals = Proposal.query.filter_by()
    authors = []
    for proposal in proposals:
        user = User.query.filter_by(id = proposal.author).first()
        authors.append(user.username)
    authors.reverse()
    
    return render_template("publish_proposal.html", title='Publish Proposal', proposals = proposals, authors = authors)


@app.route('/publish_proposal/<int:id>', methods=['GET', 'POST'])
@login_required
@isAdmin()
def publishProposals(id):
    if not isinstance(dateRank, str):
        if dateRank < date.today():
            flash('deadline has passed!','danger')
            return redirect(url_for('index'))
    proposal = Proposal.query.get_or_404(id)
    
    try:
        if proposal.published:
            proposal.published = False
        else:
            proposal.published = True
            
        db.session.commit()
        
        return redirect(url_for('publishProposal'))


    except:
        # Return an error message
        flash("Whoops! There was a problem, try again...", 'danger')

        return redirect(url_for('publishProposal'))
    
    

@app.route('/rank', methods=['GET', 'POST'])
@login_required
@isStudent()
@isLeader()
def rank():
    if current_user.member is None:
        return redirect(url_for('group'))
    if not isinstance(dateRank, str):
        if dateRank < date.today():
                flash('deadline has passed!','danger')
                return redirect(url_for('index'))
    group = Group.query.filter_by(id = current_user.member).first()
    if group.ranked:
        flash('already submitted!','danger')
        return redirect(url_for('index'))
    Session = sessionmaker(bind=db.engine)
    session = Session()
    proposals = session.query(Proposal)
    Fmember = session.query(User)

    Arr1 = []


    for proposal in proposals:
        if proposal.published == True:
            id = proposal.id
            title = proposal.title
            fid = proposal.author
            for fmember in Fmember:
                if fmember.id == fid:
                    fName = fmember.username
            Arr1.append(( id,title,fName))

    if request.method == 'POST':
        rankDict = dict()
        rankDict = request.form
        toplist = []
        group = Group.query.filter_by(id = current_user.member).first()
        members = group.members
        sum = 0
        for member in members:
            sum += member.gpa
        count = User.query.filter_by(member = group.id).count()
        avg = sum/count
        group.gpa = avg
        toplist.append(avg)
        toplist.append(current_user.member)
        temp = list(rankDict.values())
        toplist += temp
        if len(toplist) != 12:
            abort(400)
        
        group.ranked = True
        db.session.commit()


        with open('rankings.csv', 'a', newline='') as File:
            writer = csv.writer(File)
            writer.writerow(toplist)
        
    return render_template('ranking.html', data=Arr1)




@app.route('/assign_project', methods=['GET', 'POST'])
@login_required
@isAdmin()
def assign_project():
    if request.method == 'POST':
        super_list = []
        taken = []  
        with open('rankings.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                super_list.append(row)

        # Sort the sublists based on the highest first index
        super_list.sort(key=lambda x: float(x[0]), reverse=True)

        # Return the second element (Group_ID) of each sublist and its first avilable element (Project_ID) in pairs
        no_project = []
        for sublist in super_list:
            for i in range(2, len(sublist)):
                if sublist[i] not in taken:
                    group = Group.query.filter_by(id = sublist[1]).first()
                    prop = Proposal.query.filter_by(id = sublist[i]).first()
                    proposal = group.holder
                    proposal.append(prop)
                    group.set_proposal(proposal)
                    prop.owned = True
                    db.session.commit()
                    taken.append(sublist[i])
                    break


        Session = sessionmaker(bind=db.engine)
        session = Session()
        proposals = session.query(Proposal)

        all_proposals =[]

        for proposal in proposals:
            id = str(proposal.id)
            all_proposals.append(id)
        

        groups = Group.query.filter_by(ranked = False)
        for group in groups:
            prop = Proposal.query.filter_by(owned = False).first()
            proposal= [prop]
            group.set_proposal(proposal)
            prop.owned = True
            group.ranked = True
            db.session.commit()
        flash("Proposals Assigned", 'success')
        return redirect(url_for("index"))

    group = Group.query.filter_by().first()
    if group.holder:
        flash("Proposals Already Assigned", 'info')
        return redirect(url_for("index")) 

    return render_template('assign_project.html')


@app.route('/faculty_view_group', methods=['GET', 'POST'])
@login_required
@isFaculty()
def facultyView():
    proposals = Proposal.query.filter_by(author = current_user.id)
    groups = []
    addresses = []
    address = ""
    for proposal in proposals:
        group = Group.query.filter_by(id = proposal.holder).first()
        
        if group is not None:
            # group.score = -1
            # db.session.commit()
            groups.append(group)
            members = group.members
            for member in members:
                address += str(member.email)
                address += str(",")
            address = address.rstrip(",")
            addresses.append(address)
            addresses.reverse()
        

    return render_template("assigned_group.html", title='Proposal', groups=groups, addresses = addresses)


@app.route('/evaluate/<int:id>', methods=['GET', 'POST'])
@login_required
@isFaculty()
def evaluate(id):
    form = evaluateForm()
    group = Group.query.filter_by(id = id).first()
    try:
        if form.validate_on_submit():
            group.score = int(form.s1.data) + int(form.s2.data) + int(form.s3.data) + int(form.s4.data) + int(form.s5.data) + int(form.s6.data) + int(form.s7.data) + int(form.s8.data) + int(form.s9.data) + int(form.s10.data) + int(form.s11.data) + int(form.s12.data) + int(form.s13.data) + int(form.s14.data) + int(form.s15.data) + int(form.s16.data) + int(form.s17.data)
            db.session.commit()

            # Return a message
            flash("Group was evaulted!",'info')

            return redirect(url_for('facultyView'))


    except:
        # Return an error message
        flash("Whoops! There was a problem evaulting group, try again...", 'danger')

        return redirect(url_for('facultyView'))
    return render_template("evaluate.html", title='evaluate', form = form)