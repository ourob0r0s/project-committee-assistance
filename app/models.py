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

    admin = db.Column(db.Boolean, default=False)
    faculty = db.Column(db.Boolean, default=False)
    student = db.Column(db.Boolean, default=False)
    leader = db.Column(db.Boolean, default=False)

    sId = db.Column(db.Integer)
    gpa = db.Column(db.Float)


    member = db.Column(db.Integer, db.ForeignKey('group.id'))

    pId = db.relationship('Proposal', backref='user', lazy=True)
    
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
    owned = db.Column(db.Boolean, default=False)


    fId = db.Column(db.Integer, db.ForeignKey('user.id')) 
    gId = db.Column(db.Integer, db.ForeignKey('group.id')) 
    

    def __repr__(self):
        return '<Proposal {}>'.format(self.title)



class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpa = db.Column(db.Float)
    name = db.Column(db.String(20), nullable=False, unique=True)
    score = db.Column(db.Integer)


    sId = db.relationship('User', backref='group', lazy=True) 
    pId = db.relationship('Proposal', backref='group', lazy=True) 
    

    def __repr__(self):
        return '<Group {}>'.format(self.name)