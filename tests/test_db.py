import unittest
from datetime import date as Date
from random import randint
from flask import current_app
from app import create_app, db
from app.models import User
from app.surveymodels import Patient, FOLLOWUP

class VirtualFillTestCase(unittest.TestCase):
    def setUp(self):
        # initializ app
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
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
            recorder=self.test_user)
        db.session.add(self.test_patient)
        db.session.commit()
        # create follow_ups
        follow_ups = [FOLLOWUP(p_id=self.test_patient.id,
            status='v{}'.format(i), follow_up_date=Date(2017, 11, i),
            follow_up_way=2) for i in range(1, 9)]
        db.session.add_all(follow_ups)
        db.session.commit()       
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_dsss(self):
        from app.surveymodels import DSSS
        data = {'q_{}'.format(i):randint(0, 4) for i in range(1, 23)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(DSSS(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_qids(self):
        from app.surveymodels import QIDS
        data = {'q_{}'.format(i):randint(0, 4) for i in range(1, 17)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(QIDS(**data))
        db.session.commit()
        
    def test_pain(self):
        from app.surveymodels import PAIN
        data = {'q_{}'.format(i):randint(0, 4) for i in range(2, 5)}
        data.update(p_id=self.test_patient.id, status='v2', q_1='abcd')
        db.session.add(PAIN(**data))
        db.session.commit()
        
    def test_mfi_20(self):
        from app.surveymodels import MFI
        data = {'q_{}'.format(i):randint(0, 5) for i in range(1, 21)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(MFI(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_psqi(self):
        from app.surveymodels import PSQI
        data = dict()
        for i in range(1, 10):
            if i == 5:
                for j in range(1, 11):
                    data['q_{}_{}'.format(i, j)] = randint(0, 4)
            else:
                data['q_{}'.format(i)] = randint(0, 4)
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(PSQI(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_meq_sa(self):
        from app.surveymodels import MEQ_SA
        data = {'q_{}'.format(i):randint(0, 5) for i in range(1, 20)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(MEQ_SA(**data))
        self.assertTrue(db.session.commit() is None)
    
    def text_staxi_2(self):
        from app.surveymodels import STAXI_2
        data = {'q_{}'.format(i):randint(0, 4) for i in range(1, 58)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(STAXI_2(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_ipas(self):
        from app.surveymodels import IPAS
        data = {'q_{}'.format(i):randint(0, 4) for i in range(1, 31)}
        data.update(p_id=self.test_patient.id, status='v2')
        db.session.add(IPAS(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_mdq(self):
        from app.surveymodels import MDQ
        data = {'q_1_{}'.format(i):randint(1, 2) for i in range(1, 14)}
        data.update(dict(q_2=2, q_3=3, p_id=self.test_patient.id, status='v2'))
        db.session.add(MDQ(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_ssp(self):
        from app.surveymodels import SSP
        data = {'q_{}'.format(i):randint(1, 4) for i in range(1, 92)}
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(SSP(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_pbi(self):
        from app.surveymodels import PBI
        data = {'q_{}'.format(i):randint(1, 4) for i in range(1, 26)}
        data.update(dict(p_id=self.test_patient.id, status='v2', parent='父亲'))
        db.session.add(PBI(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_ssp(self):
        from app.surveymodels import CTQ
        data = {'q_{}'.format(i):randint(1, 5) for i in range(1, 29)}
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(CTQ(**data))
        self.assertTrue(db.session.commit() is None)
        
    def test_les(self):
        from app.surveymodels import LES
        data = dict(event_code=2, event_date=3, property=1, degree=1, duration=2, note='NOTE')
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(LES(**data))
        self.assertTrue(db.session.commit () is None)
        
    def test_inout(self):
        from app.surveymodels import InOut
        data = dict(q_1 = 'abcd', q_2='')
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(InOut(**data))
        self.assertTrue(db.session.commit () is None)
        
    def test_hamd(self):
        from app.surveymodels import HAMD
        data = {'q_{}'.format(i):randint(1, 4) for i in range(1, 18)}
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(HAMD(**data))
        self.assertTrue(db.session.commit () is None)
        
    def test_ymrs(self):
        from app.surveymodels import YMRS
        data = {'q_{}'.format(i):randint(1, 4) for i in range(1, 12)}
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(YMRS(**data))
        self.assertTrue(db.session.commit () is None)
        
    def test_cgi(self):
        from app.surveymodels import CGI
        data = {'q_{}'.format(i):randint(1, 4) for i in range(1, 4)}
        data.update(dict(p_id=self.test_patient.id, status='v2'))
        db.session.add(CGI(**data))
        self.assertTrue(db.session.commit () is None)
        
    def test_body_exam(self):
        from app.surveymodels import BODY_EXAM
        data = {'q_{}'.format(i):randint(1, 4) for i in range(2, 8)}
        data.update(dict(p_id=self.test_patient.id, status='v2', q_1_1=120, q_1_2=80))
        db.session.add(BODY_EXAM(**data))
        self.assertTrue(db.session.commit () is None)