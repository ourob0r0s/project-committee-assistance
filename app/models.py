from app import db
# todo nullable


class Faculty_member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    publish = db.Column(db.Boolean, default=False, nullable=False)
    deadline = db.Column(db.Boolean, default=False, nullable=False)
    authorize = db.Column(db.Boolean, default=False, nullable=False)
    studentCount = db.Column(db.Boolean, default=False, nullable=False)
    postedPropsal = db.relationship('Propsal', backref='faculty_member', lazy=True)
    postedStudentReport = db.relationship('Individual_report', backref='faculty_member', lazy=True)
    postedGroupReport =  db.relationship('Group_report', backref='faculty_member', lazy=True)


    def __repr__(self):
        return '<Faculty member {}>'.format(self.username)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    sId = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    groupOwner = db.relationship('Group', backref='student', lazy=True)
    member = db.Column(db.Integer, db.ForeignKey('student.id'))
    studentReport = db.relationship('Individual_report', backref='student', lazy=True)



    def __repr__(self):
        return '<Student {}>'.format(self.sId)

class Propsal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    desc = db.Column(db.String(2064), index=True, unique=True)
    fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'),nullable=False) #fk
    gId = db.Column(db.Integer, db.ForeignKey('group.id'),nullable=False) #fk
    

    def __repr__(self):
        return '<Propsal {}>'.format(self.title)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpa = db.Column(db.Float)
    owner = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False) #fk
    member = db.relationship('Student', backref='group', lazy=True) #fk
    ownedPropsal = db.relationship('Propsal', backref='group', lazy=True) #fk
    groupReport = db.relationship('Group_report', backref='group', lazy=True)
    code = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Group {}>'.format(self.id)

class Individual_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'),nullable=False)
    sId = db.Column(db.Integer, db.ForeignKey('student.id'),nullable=False)
    
    def __repr__(self):
        return '<Individual_report {}>'.format(self.id)

class Group_report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    fId = db.Column(db.Integer, db.ForeignKey('faculty_member.id'),nullable=False)
    gId = db.Column(db.Integer, db.ForeignKey('group.id'),nullable=False)
    
    def __repr__(self):
        return '<Group_report {}>'.format(self.id)


