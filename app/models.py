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
        
class PAIN(db.Model, Export):
    __tablename__ = 'pain'
    export_cols = ('p_id', 'status','q_1', 'q_2', 'q_3', 'q_4')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1 = db.Column(db.String(16))
    q_2 = db.Column(db.Integer)
    q_3 = db.Column(db.Integer)
    q_4 = db.Column(db.Integer)
    
    def __repr__(self):
        return '<PAIN {}>'.format(self.id)
 
class MFI(db.Model, Export):
    __tablename__ = 'mfi_20'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9', 'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20')
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
    
class PSQI(db.Model, Export):
    __tablename__ = 'psqi'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 
    'q_5_1', 'q_5_2', 'q_5_3', 'q_5_4', 'q_5_5', 'q_5_6', 'q_5_7', 'q_5_8', 'q_5_9', 'q_5_10',
    'q_6', 'q_7', 'q_8', 'q_9')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1 = db.Column(db.Integer)
    q_2 = db.Column(db.Integer)
    q_3 = db.Column(db.Integer)
    q_4 = db.Column(db.Integer)
    q_5_1 = db.Column(db.Integer)
    q_5_2 = db.Column(db.Integer)
    q_5_3 = db.Column(db.Integer)
    q_5_4 = db.Column(db.Integer)
    q_5_5 = db.Column(db.Integer)
    q_5_6 = db.Column(db.Integer)
    q_5_7 = db.Column(db.Integer)
    q_5_8 = db.Column(db.Integer)
    q_5_9 = db.Column(db.Integer)
    q_5_10 = db.Column(db.Integer)
    q_6 = db.Column(db.Integer)
    q_7 = db.Column(db.Integer)
    q_8 = db.Column(db.Integer)
    q_9 = db.Column(db.Integer)
    
class MEQ_SA(db.Model, Export):
    __tablename__ = 'meq_sa'
    export_cols = export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9', 'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19')
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

class STAXI_2(db.Model, Export):
    __tablename__ = 'staxi_2'
    export_cols = ('p_id', 'status','q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9',
    'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20', 'q_21',
    'q_22', 'q_23', 'q_24', 'q_25', 'q_26', 'q_27', 'q_28', 'q_29', 'q_30', 'q_31', 'q_32', 'q_33',
    'q_34', 'q_35', 'q_36', 'q_37', 'q_38', 'q_39', 'q_40', 'q_41', 'q_42', 'q_43', 'q_44', 'q_45',
    'q_46', 'q_47', 'q_48', 'q_49', 'q_50', 'q_51', 'q_52', 'q_53', 'q_54', 'q_55', 'q_56', 'q_57')
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
    q_23 = db.Column(db.Integer)
    q_24 = db.Column(db.Integer)
    q_25 = db.Column(db.Integer)
    q_26 = db.Column(db.Integer)
    q_27 = db.Column(db.Integer)
    q_28 = db.Column(db.Integer)
    q_29 = db.Column(db.Integer)
    q_30 = db.Column(db.Integer)
    q_31 = db.Column(db.Integer)
    q_32 = db.Column(db.Integer)
    q_33 = db.Column(db.Integer)
    q_34 = db.Column(db.Integer)
    q_35 = db.Column(db.Integer)
    q_36 = db.Column(db.Integer)
    q_37 = db.Column(db.Integer)
    q_38 = db.Column(db.Integer)
    q_39 = db.Column(db.Integer)
    q_40 = db.Column(db.Integer)
    q_41 = db.Column(db.Integer)
    q_42 = db.Column(db.Integer)
    q_43 = db.Column(db.Integer)
    q_44 = db.Column(db.Integer)
    q_45 = db.Column(db.Integer)
    q_46 = db.Column(db.Integer)
    q_47 = db.Column(db.Integer)
    q_48 = db.Column(db.Integer)
    q_49 = db.Column(db.Integer)
    q_50 = db.Column(db.Integer)
    q_51 = db.Column(db.Integer)
    q_52 = db.Column(db.Integer)
    q_53 = db.Column(db.Integer)
    q_54 = db.Column(db.Integer)
    q_55 = db.Column(db.Integer)
    q_56 = db.Column(db.Integer)
    q_57 = db.Column(db.Integer)