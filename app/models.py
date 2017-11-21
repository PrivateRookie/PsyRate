# -*- coding: utf-8 -*-
from . import db
from . import login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    patients = db.relationship('Patient', backref='recorder_lookup')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class Patient(db.Model):
    __tablename__ = 'patient_infos'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(32))
    entry_date = db.Column(db.Date)
    doctor = db.Column(db.String(32))
    recorder = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return '<Patient {}>'.format(self.name)   
    
class FollowUp(db.Model):
    __tablename__ = 'follow_ups'
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16))
    follow_up_date = db.Column(db.Date)
    follow_up_way = db.Column(db.Integer)
    
    def __repr__(self):
        return '<FollowUP {}>'.format(self.status)
    
class QIDS(db.Model):
    __tablename__ = 'qids_sr16'
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1 = db.Column(db.Integer)
    q_2 = db.Column(db.Integer)
    q_3 = db.Column(db.Integer)
    q_4 = db.Column(db.Integer)
    q_5 = db.Column(db.Integer)
    q_6 = db.Column(db.Integer)
    q_7 = db.Column(db.Integer)
    q_8 = db.Column(db.Integer)
    q_9 = db.Column(db.Integer)
    q_10 = db.Column(db.Integer)
    q_11 = db.Column(db.Integer)
    q_12 = db.Column(db.Integer)
    q_13 = db.Column(db.Integer)
    q_14 = db.Column(db.Integer)
    q_15 = db.Column(db.Integer)
    q_16 = db.Column(db.Integer)
    
    def __repr__(self):
        return '<QIDS {}>'.format(self.id)
        
class DSSS(db.Model):
    __tablename__ = 'dsss'
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1 = db.Column(db.Integer)
    q_2 = db.Column(db.Integer)
    q_3 = db.Column(db.Integer)
    q_4 = db.Column(db.Integer)
    q_5 = db.Column(db.Integer)
    q_6 = db.Column(db.Integer)
    q_7 = db.Column(db.Integer)
    q_8 = db.Column(db.Integer)
    q_9 = db.Column(db.Integer)
    q_10 = db.Column(db.Integer)
    q_11 = db.Column(db.Integer)
    q_12 = db.Column(db.Integer)
    q_13 = db.Column(db.Integer)
    q_14 = db.Column(db.Integer)
    q_15 = db.Column(db.Integer)
    q_16 = db.Column(db.Integer)
    q_17 = db.Column(db.Integer)
    q_18 = db.Column(db.Integer)
    q_19 = db.Column(db.Integer)
    q_20 = db.Column(db.Integer)
    q_21 = db.Column(db.Integer)
    q_22 = db.Column(db.Integer)
    
    def __repr__(self):
        return '<DSSS {}>'.format(self.id)
 