from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Faculty_member,Student

class facultyLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class studentLoginForm(FlaskForm):
    id = IntegerField('student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class facultyRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        faculty_member = Faculty_member.query.filter_by(username=username.data).first()
        student = Student.query.filter_by(username=username.data).first()
        if faculty_member or student is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        faculty_member = Faculty_member.query.filter_by(email=email.data).first()
        student = Student.query.filter_by(email=email.data).first()
        if faculty_member or student is not None:
            raise ValidationError('Please use a different email address.')
    
class studentRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    id = IntegerField('student ID', validators=[DataRequired()])
    gpa = FloatField('student gpa', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        faculty_member = Faculty_member.query.filter_by(username=username.data).first()
        student = Student.query.filter_by(username=username.data).first()
        if faculty_member or student is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, id):
        student = Student.query.filter_by(id=id.data).first()
        if student is not None:
            raise ValidationError('Please use a different student id.')