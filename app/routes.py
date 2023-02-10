from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import studentLoginForm, facultyLoginForm, facultyRegisterForm, studentRegisterForm, proposalAdd, groupAdd, groupJoin
from app.models import User, Proposal, Group
from app.decorators import isFaculty, isAdmin, isStudent, isLeader
from sqlalchemy.orm import sessionmaker
from array import *
import csv
#todo prop group count
@app.route('/')
@app.route('/index')
def index():
    current_user.leader = True
    db.session.commit()
    return render_template("index.html", title='Home Page')


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
        userNow = user
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
        userNow = user
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


@app.route('/proposal', methods=['GET', 'POST'])
@login_required
@isFaculty()
def proposal():

    proposals = Proposal.query.filter_by(author = current_user.id)
    
    return render_template("proposal.html", title='Proposal', proposals=proposals)


@app.route('/add_proposal', methods=['GET', 'POST'])
@login_required
@isFaculty()
def addProposal():
    form = proposalAdd()
    if form.validate_on_submit():
        prop = Proposal(title= form.title.data, desc=form.desc.data)
        db.session.add(prop)
        db.session.commit()

        prop = Proposal.query.filter_by(title = form.title.data).first()
        props = current_user.author
        props.append(prop)
        current_user.set_author(props)
        print(prop.author)
        flash('Congratulations, your proposal has been added!','success')
        return redirect(url_for('proposal'))
    return render_template("add_proposal.html", title='add Proposal', form=form)



@app.route('/proposal/delete/<int:id>')
@login_required
@isFaculty()
def deleteProposal(id):
    proposal = Proposal.query.get_or_404(id)
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
    if form.validate_on_submit():
        group = Group.query.filter_by(name = form.name.data).first()
        members = group.members
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
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        db.session.add(group)
        current_user.leader = True
        db.session.commit()

        group = Group.query.filter_by(name = form.name.data).first()
        members = group.members
        members.append(current_user)
        group.set_member(members)
        

        print(group.members)
        flash('Congratulations, you have created a group!', 'success')
        return redirect(url_for('group'))
    return render_template("add_group.html", title='Create group', form=form)


@app.route('/group/delete/<int:id>')
@login_required
@isStudent()
@isLeader()
def deleteGroup(id):
    group = Group.query.get_or_404(id)
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




@app.route('/group/remove/<int:id>')
@login_required
@isStudent()
@isLeader()
def removeMember(id):
    if current_user.id != id:
        user = User.query.get_or_404(id)
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
def publishProposal():
    
    proposals = Proposal.query.filter_by()
    
    return render_template("publish_proposal.html", title='Publish Proposal', proposals = proposals)


@app.route('/publish_proposal/<int:id>', methods=['GET', 'POST'])
@login_required
def publishProposals(id):
    proposal = Proposal.query.get_or_404(id)
    
    try:
        if proposal.published:
            print(1)
            proposal.published = False
        else:
            print(0)
            proposal.published = True
            
        db.session.commit()
        
        return redirect(url_for('publishProposal'))


    except:
        # Return an error message
        flash("Whoops! There was a problem, try again...", 'danger')

        return redirect(url_for('publishProposal'))
    
    

@app.route('/r', methods=['GET', 'POST'])
def rank():

    Session = sessionmaker(bind=db.engine)
    session = Session()
    proposals = session.query(Proposal)
    Fmember = session.query(User)

    Arr1 = []


    for proposal in proposals:
        id = proposal.id
        title = proposal.title
        fid = proposal.author
        for fmember in Fmember:
            if fmember.id == fid:
                fName = fmember.username
        Arr1.append(( id,title,fName))




    return render_template('ranking.html', data=Arr1)


@app.route('/writefile', methods=['POST'])
def writefile():
    print("2")
    if request.method == 'POST':
        rankDict = dict()
        rankDict = request.form
        toplist = []
        group = Group.query.filter_by(id = current_user.member).first()
        members = group.members
        sum = 0
        for member in members:
            sum += member.gpa
        avg = sum/3
        group.gpa = avg
        db.session.commit()
        toplist.append(avg)
        toplist.append(current_user.member)
        temp = list(rankDict.values())
        toplist += temp
        
        
        if len(toplist) != 5:
            print("9")
            flash("Whoops! There was a problem deleting proposal, try again...", 'danger')
            print("5")
            return ""


        print(toplist)
        with open('rankings.csv', 'a', newline='') as File:
            writer = csv.writer(File)
            writer.writerow(toplist)
        return ""
