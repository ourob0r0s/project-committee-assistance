from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import Faculty_member,Student

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FacultyRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        faculty_member = Faculty_member.query.filter_by(username=username.data).first()
        student = Student.query.filter_by(username=username.data).first()
        if Faculty_member or Student is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        faculty_member = Faculty_member.query.filter_by(email=email.data).first()
        student = Student.query.filter_by(email=email.data).first()
        if Faculty_member or Student is not None:
            raise ValidationError('Please use a different email address.')
    
class StudentRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        faculty_member = Faculty_member.query.filter_by(username=username.data).first()
        student = Student.query.filter_by(username=username.data).first()
        if Faculty_member or Student is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        faculty_member = Faculty_member.query.filter_by(email=email.data).first()
        student = Student.query.filter_by(email=email.data).first()
        if Faculty_member or Student is not None:
            raise ValidationError('Please use a different email address.')