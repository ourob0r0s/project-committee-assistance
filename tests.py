import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import app, db
from app.models import User,Proposal,Group

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
        proposal = Proposal(title='title1', desc='desc')
        db.session.add(proposal)
        group = Group(name="cold")
        db.session.add(group)
        db.session.commit()
        
        user = User(username='musab', email='museab@yahoo.com', faculty = True)
        user.set_password('cat')
        proposal = Proposal.query.filter_by(id=1).first()
        user.set_author([proposal])
        db.session.add(user)
        user = User(username='khaled', email='daf@yahoo.com', student = True)
        user.set_password('cat')
       
        db.session.add(user)
        db.session.commit() 
        group = Group.query.filter_by(id=1).first()
        user = User.query.filter_by(id=2).first()
        group.set_member([user])


        

        

if __name__ == '__main__':
    unittest.main(verbosity=2)