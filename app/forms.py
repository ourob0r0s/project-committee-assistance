from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Group, Proposal
#todo vaildators, message

class groupJoin(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min= 3, max= 20, message ="")])
    submit = SubmitField('Join')

    def validate_name(self, name):
        group = Group.query.filter_by(name=name.data).first()
        if group is None:
            raise ValidationError('Please check if the name is correct.')


class groupAdd(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min= 3, max= 20, message ="")])
    submit = SubmitField('Create')

    def validate_name(self, name):
        group = Group.query.filter_by(name=name.data).first()
        if group is not None:
            raise ValidationError('Please use a different name.')


class proposalAdd(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(min= 1, max= 20, message ="")])
    desc = TextAreaField('description', validators=[DataRequired(), Length(min= 1 , message="")])
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
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
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
    username = StringField('Username', validators=[DataRequired()])
    sId = IntegerField('student ID', validators=[DataRequired()])
    gpa = FloatField('student gpa', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
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
