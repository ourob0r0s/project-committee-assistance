from app import db
from app import login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Faculty_member(User,db.Model):
    publish = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.Boolean, default=False)
    authorize = db.Column(db.Boolean, default=False)
    studentCount = db.Column(db.Boolean, default=False)

    postedPropsal = db.relationship('Propsal', backref='User', lazy=True)
    postedStudentReport = db.relationship('Individual_report', backref='User', lazy=True)
    postedGroupReport =  db.relationship('Group_report', backref='User', lazy=True)


    def __repr__(self):
        return '<Faculty member {}>'.format(self.username)

class Student(User,db.Model):
    sId = db.Column(db.Integer , nullable=False)
    gpa = db.Column(db.Float , nullable=False)

    groupOwner = db.relationship('Group', backref='User', lazy=True)
    member = db.Column(db.Integer, db.ForeignKey('user.id'))
    studentReport = db.relationship('Individual_report', backref='User', lazy=True)

   
    def __repr__(self):
        return '<Student {}>'.format(self.sId)

class Propsal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True, nullable=False)
    desc = db.Column(db.String(2064), index=True, unique=True, nullable=False)

    fId = db.Column(db.Integer, db.ForeignKey('user.id')) 
    gId = db.Column(db.Integer, db.ForeignKey('group.id')) 
    

    def __repr__(self):
        return '<Propsal {}>'.format(self.title)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpa = db.Column(db.Float, nullable=False)
    code = db.Column(db.Integer, nullable=False)

    owner = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    member = db.relationship('User', backref='group', lazy=True) 
    ownedPropsal = db.relationship('Propsal', backref='group', lazy=True) 
    groupReport = db.relationship('Group_report', backref='group', lazy=True)
    

    def __repr__(self):
        return '<Group {}>'.format(self.id)

class Individual_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    fId = db.Column(db.Integer, db.ForeignKey('user.id'))
    sId = db.Column(db.Integer, db.ForeignKey('user.id'))
    

    def __repr__(self):
        return '<Individual_report {}>'.format(self.id)

class Group_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    fId = db.Column(db.Integer, db.ForeignKey('user.id'))
    gId = db.Column(db.Integer, db.ForeignKey('group.id'))
    

    def __repr__(self):
        return '<Group_report {}>'.format(self.id)


