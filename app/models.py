from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    publish = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Boolean, default=False)
    authorize = db.Column(db.Boolean, default=False)
    studentCount = db.Column(db.Boolean, default=False)

    sId = db.Column(db.Integer)
    gpa = db.Column(db.Float)

    # studentReport = db.relationship('Individual_report', backref='student', lazy=True)
    member = db.Column(db.Integer, db.ForeignKey('group.id'))

    postedProposal = db.relationship('Proposal', backref='user', lazy=True)
    # postedStudentReport = db.relationship('Individual_report', backref='faculty_member', lazy=True)
    # postedGroupReport =  db.relationship('Group_report', backref='faculty_member', lazy=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)



class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True,)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    desc = db.Column(db.String(2064), index=True, unique=True, nullable=False)
    published = db.Column(db.Boolean, default=False)

    fId = db.Column(db.Integer, db.ForeignKey('user.id')) 
    gId = db.Column(db.Integer, db.ForeignKey('group.id')) 
    

    def _repr_(self):
        return '<Proposal {}>'.format(self.title)



class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpa = db.Column(db.Float)
    name = db.Column(db.String(20), nullable=False, unique=True)
    ownerId = db.Column(db.Integer)

    sId = db.relationship('User', backref='group', lazy=True) 
    ownedProposal = db.relationship('Proposal', backref='group', lazy=True) 
    # groupReport = db.relationship('Group_report', backref='group', lazy=True)
    

    def _repr_(self):
        return '<Group {}>'.format(self.id)



class Individual_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    
    # fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'))
    # sId = db.Column(db.Integer, db.ForeignKey('student.id'))
    

    def _repr_(self):
        return '<Individual_report {}>'.format(self.id)



class Group_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    # fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'))
    # gId = db.Column(db.Integer, db.ForeignKey('group.id'))
    

    def _repr_(self):
        return '<Group_report {}>'.format(self.id)


