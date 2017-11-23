import unittest
from datetime import date as Date
from random import randint
from flask import current_app
from app import create_app, db
from app.models import User, Patient, FollowUp

class VirtualFillTestCase(unittest.TestCase):
    def setUp(self):
        # initializ app
        #self.app = create_app('test')
        #self.app_context = self.app.app_context()
        #self.app_context.push()
        # initializ database
        db.drop_all()
        db.create_all()
        # create test user
        self.test_user = User(username="Test_User", email="test@test.com",
            password='PsyRatesTest')
        db.session.add(self.test_user)
        db.session.commit()
        # create test patient
        self.test_patient = Patient(code='TEST001', name='Test',
            entry_date=Date(2017,11,21), doctor='Test Doctor',
            recorder=self.test_user.id)
        db.session.add(self.test_patient)
        db.session.commit()
        # create follow_ups
        follow_ups = [FollowUp(p_id=self.test_patient.id,
            status='v{}'.format(i), follow_up_date=Date(2017, 11, i),
            follow_up_way=2) for i in range(1, 9)]
        db.session.add_all(follow_ups)
        db.session.commit()       
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #self.app_context.pop()
        
    def test_dsss(self):
        from app.models import DSSS
        data = {'q_{}'.format(i):randint(0, 4) for i in range(1, 23)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(DSSS(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_qids(self):
        from app.models import QIDS
        data = {'q_{}'.format(i):randint(0, 4) for i in range(1, 17)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(QIDS(**data))
        db.session.commit()
        
    def test_pain(self):
        from app.models import PAIN
        data = {'q_{}'.format(i):randint(0, 4) for i in range(2, 5)}
        data.update(p_id=self.test_patient.id, status='v2', q_1='abcd')
        db.session.add(PAIN(**data))
        db.session.commit()