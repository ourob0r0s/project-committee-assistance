from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, TextAreaField, DateField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange
from app.models import User, Group, Proposal



class evaluateForm(FlaskForm):
    s1 = RadioField('Organization of report (title page, abstract, table of contents, reference list, ...)', choices=[1,2], validators=[DataRequired()])
    s2 = RadioField('Introduction, motivations, objectives, and literature review', choices=[1,2], validators=[DataRequired()])
    s3 = RadioField('Description of proposed project functional and non-functional requirements', choices=[1,2,3], validators=[DataRequired()])
    s4 = RadioField('Usage of project particular management tools such as Gantt chart, WBS, etc.', choices=[1], validators=[DataRequired()])
    s5 = RadioField('Following of particular information system development methodology such as SDLC, agile, etc.	', choices=[1], validators=[DataRequired()])
    s6 = RadioField('Usage of diagrams such as ER, use case, class diagram, etc.', choices=[1,2,3,4,5,6], validators=[DataRequired()])
    s7 = RadioField('Completion of all project requirements (functional and non-functional).', choices=[1,2,3,4], validators=[DataRequired()])
    s8 = RadioField('Professional (clear, complete and consistence) presentation of the proposed system.', choices=[1,2,3,4], validators=[DataRequired()])
    s9 = RadioField('Quality (logical and correctness) of the proposed system.', choices=[1,2,3,4,5,6,7], validators=[DataRequired()])
    s10 = RadioField('Difficulty and size of the work.', choices=[1,2,3,4,5], validators=[DataRequired()])
    s11 = RadioField('Students presentation Skills.', choices=[1,2], validators=[DataRequired()])
    s12 = RadioField('Ability of students to answer questions about the analysis and design of the system.', choices=[1,2,3], validators=[DataRequired()])
    submit = SubmitField('Confirm')

class deadlineSet(FlaskForm):
    dateProposal = DateField('propoosal Date', validators=[DataRequired()])
    dateRank = DateField('ranking Date', validators=[DataRequired()])
    submit = SubmitField('confirm')


class groupJoin(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Join')

    def validate_name(self, name):
        group = Group.query.filter_by(name=name.data).first()
        if group is None:
            raise ValidationError('Please check if the name is correct.')


class groupAdd(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min= 3, max= 20, message ="name should be 3 to 20 characters")])
    submit = SubmitField('Create')

    def validate_name(self, name):
        group = Group.query.filter_by(name=name.data).first()
        if group is not None:
            raise ValidationError('Please use a different name.')


class proposalAdd(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min= 1, max= 30, message ="title should be 7 to 30 characters")])
    desc = TextAreaField('description', validators=[DataRequired(), Length(min= 1, max = 2064, message="description should be 30 to 2064 characters")])
    submit = SubmitField('add proposal')


class facultyLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class studentLoginForm(FlaskForm):
    sId = IntegerField('student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class facultyRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min= 1, max= 64, message ="username should be 3 to 64 characters")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min= 1, max= 64, message ="password should be 8 to 64 characters")])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class studentRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min= 1, max= 64, message ="username should be 3 to 64 characters")])
    # min= 430000000, max= 499999999, message ="please enter a correct student id"
    sId = IntegerField('student ID', validators=[DataRequired(), NumberRange(min= 0, message ="please enter a correct student id")])
    gpa = FloatField('student gpa', validators=[DataRequired(), NumberRange(min= 2, max= 5, message ="please enter a correct gpa")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min= 1, max= 64, message ="password should be 8 to 64 characters")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, sId):
        user = User.query.filter_by(sId=sId.data).first()
        if user is not None:
            raise ValidationError('Please use a different student id.')
