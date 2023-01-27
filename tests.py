import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import app, db
from app.models import User,Proposal,Group,Individual_report,Group_report

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
        


    def test_models(self):
        user = User(username='mussab', email='museab@yahoo.com')
        user.set_password('cat')
        db.session.add(user)
        proposal = Proposal(title='title1', desc='desc')
        db.session.add(proposal)
        group = Group(code=1234567890)
        db.session.add(group)
        individual_report = Individual_report(score=50)
        db.session.add(individual_report)
        group_report = Group_report(score=50)
        db.session.add(group_report)
        db.session.commit()
        print(User.query.all())

    # def test_relationships(self):
    #     student = Student(id = 1,username='musab', email='musab@yahoo.com', gpa=4.54)
    #     student.set_password('cat')
    #     db.session.add(student)
    #     faculty = Faculty_member(id = 1,username='musab', email='musab@yahoo.com')
    #     faculty.set_password('dog')
    #     db.session.add(faculty)
    #     proposal = Proposal(id = 1,title='title1', desc='desc')
    #     db.session.add(proposal)
    #     group = Group(id = 1,code=1234567890)
    #     db.session.add(group)
    #     individual_report = Individual_report(id = 1,score=50)
    #     db.session.add(individual_report)
    #     group_report = Group_report(id = 1,score=50)
    #     db.session.add(group_report)
    #     db.session.commit()



if __name__ == '__main__':
    unittest.main(verbosity=2)