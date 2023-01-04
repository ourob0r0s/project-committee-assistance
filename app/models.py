from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#todo auto increment and group and student fk

@login.user_loader
def load_faculty(id):
    return Faculty_member.query.get(int(id))





class Faculty_member(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    publish = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Boolean, default=False)
    authorize = db.Column(db.Boolean, default=False)
    studentCount = db.Column(db.Boolean, default=False)

    postedPropsal = db.relationship('Propsal', backref='faculty_member', lazy=True)
    postedStudentReport = db.relationship('Individual_report', backref='faculty_member', lazy=True)
    postedGroupReport =  db.relationship('Group_report', backref='faculty_member', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<Faculty member {}>'.format(self.username)

class Student(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    gpa = db.Column(db.Float , nullable=False)

    studentReport = db.relationship('Individual_report', backref='student', lazy=True)
    member = db.Column(db.Integer, db.ForeignKey('group.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
            return check_password_hash(self.password_hash, password)

   
    def __repr__(self):
        return '<Student {}>'.format(self.id)

class Propsal(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    desc = db.Column(db.String(2064), index=True, unique=True, nullable=False)
    published = db.Column(db.Boolean, default=False)

    fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id')) 
    gId = db.Column(db.Integer, db.ForeignKey('group.id')) 
    

    def __repr__(self):
        return '<Propsal {}>'.format(self.title)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpa = db.Column(db.Float)
    code = db.Column(db.Integer, nullable=False)

    sId = db.relationship('Student', backref='group', lazy=True) 
    ownedPropsal = db.relationship('Propsal', backref='group', lazy=True) 
    groupReport = db.relationship('Group_report', backref='group', lazy=True)
    

    def __repr__(self):
        return '<Group {}>'.format(self.id)

class Individual_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    
    fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'))
    sId = db.Column(db.Integer, db.ForeignKey('student.id'))
    

    def __repr__(self):
        return '<Individual_report {}>'.format(self.id)

class Group_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'))
    gId = db.Column(db.Integer, db.ForeignKey('group.id'))
    

    def __repr__(self):
        return '<Group_report {}>'.format(self.id)


