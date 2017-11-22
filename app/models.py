# -*- coding: utf-8 -*-
import csv
from . import db
from . import login_manager
from flask_login import UserMixin

class Export:
    __tablename__ = None
    export_cols = None
    
    @classmethod
    def export2csv(cls, csv_file=None):
        csv_file = cls.__tablename__ + '.csv' if csv_file is None else csv_file
        ints = cls.query.all()
        col_names = ['p_id', 'status']
        col_names += [cls.__tablename__ + col for col in cls.export_cols]
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(col_names)
            for int in ints:
                line = [getattr(int, attr) for attr in cls.export_cols]
                writer.writerow(line)

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
    
class QIDS(db.Model, Export):
    __tablename__ = 'qids_sr16'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9', 'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16')
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
        
class DSSS(db.Model, Export):
    __tablename__ = 'dsss'
    export_cols = ('p_id', 'status','q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9', 'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20', 'q_21', 'q_22')
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
 