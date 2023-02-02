from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import studentLoginForm,facultyLoginForm, facultyRegisterForm,studentRegisterForm,proposalAdd,groupAdd
from app.models import User,Proposal,Group,Individual_report,Group_report
#todo titles


@app.route('/')
@app.route('/index')
def index():
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
            flash('Invalid username or password')
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
            flash('Invalid username or password')
            return redirect(url_for('facultyLogin'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/faculty_login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/student_register', methods=['GET', 'POST'])
def studentRegister():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = studentRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=(str(form.sId.data)+"@student.ksu.edu.sa"), sId=form.sId.data, gpa=form.gpa.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('studentLogin'))
    return render_template('auth/student_register.html', title='Register', form=form)

@app.route('/faculty_register', methods=['GET', 'POST'])
def facultyRegister():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = facultyRegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('facultyLogin'))
    return render_template('auth/faculty_register.html', title='Register', form=form)

@app.route('/proposal', methods=['GET', 'POST'])
def proposal():

    proposals = Proposal.query.filter_by()
    
    return render_template("proposal.html", title='Home Page', proposals=proposals)

@app.route('/add_proposal', methods=['GET', 'POST'])
def addProposal():
    form = proposalAdd()
    if form.validate_on_submit():
        prop = Proposal(title= form.title.data, desc=form.desc.data)
        db.session.add(prop)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('proposal'))
    return render_template("add_proposal.html", title='Home Page', form=form)



@app.route('/proposal/delete/<int:id>')
def deleteProposal(id):
	proposal = Proposal.query.get_or_404(id)
	# id = current_user.id
	# if id == post_to_delete.poster.id or id == 14:
	try:
			db.session.delete(proposal)
			db.session.commit()

			# Return a message
			flash("proposal Was Deleted!")

			# Grab all the posts from the database
			proposals = Proposal.query.filter_by()
			return render_template("proposal.html", proposals=proposals)


	except:
			# Return an error message
			flash("Whoops! There was a problem deleting proposal, try again...")

			# Grab all the posts from the database
			proposals = Proposal.query.filter_by()
			return render_template("proposal.html", proposals=proposals)
	# else:
	# 	# Return a message
	# 	flash("You Aren't Authorized To Delete That Proposal!")

	# 	# Grab all the posts from the database
	# 	posts = Posts.query.order_by(Posts.date_posted)
	# 	return render_template("posts.html", posts=posts)
# @app.route('/StudentHome')
# def index():
#     return render_template("SHome.html", title='Home Page')


# @app.route('/AdminHome')
# def index():
#     return render_template("AHome.html", title='Home Page')
@app.route('/group', methods=['GET', 'POST'])
def group():
    return render_template("group.html", title='Home Page')



@app.route('/add_group', methods=['GET', 'POST'])
def addGroup():
    form = groupAdd()
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        db.session.add(group)
        db.session.commit()
        flash('Congratulations, you are created a group!')
        return redirect(url_for('group'))
    return render_template("add_group.html", title='Home Page', form=form)



