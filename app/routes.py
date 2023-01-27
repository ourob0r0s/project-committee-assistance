from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import studentLoginForm,facultyLoginForm, facultyRegisterForm,studentRegisterForm
from app.models import User,Faculty_member,Student,Proposal,Group,Individual_report,Group_report



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
        student = Student.query.filter_by(id=form.id.data).first()
        if student is None or not student.check_password(form.password.data):
            flash('Invalid id or password')
            return redirect(url_for('login'))
        login_user(student, remember=form.remember_me.data)
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
        faculty = Faculty_member.query.filter_by(email=form.email.data).first()
        if faculty is None or not faculty.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('facultyLogin'))
        login_user(faculty, remember=form.remember_me.data)
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
        student = Student(username=form.username.data, email=(form.id.data+"@student.ksu.edu.sa"), id=form.id.data, gpa=form.gpa.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth/student_login'))
    return render_template('auth/student_register.html', title='Register', form=form)

@app.route('/faculty_register', methods=['GET', 'POST'])
def facultyRegister():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = facultyRegisterForm()
    if form.validate_on_submit():
        faculty = Faculty_member(username=form.username.data, email=form.email.data)
        faculty.set_password(form.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('facultyLogin'))
    return render_template('auth/faculty_register.html', title='Register', form=form)









