# -*- coding: utf-8 -*-
import csv
from . import db
from .models import Patient

class Export:
    """helper class for export database as csv file"""
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
    
class IPAS(db.Model, Export):
    __tablename__ = 'ipas'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9',
    'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20', 'q_21',
    'q_23', 'q_24', 'q_25', 'q_26', 'q_27', 'q_28', 'q_29', 'q_30')
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
    
class MDQ(db.Model, Export):
    __tablename__ = 'mdq'
    export_cols = ('p_id', 'status', 'q_1_1', 'q_1_2', 'q_1_3', 'q_1_4', 'q_1_5', 'q_1_6', 'q_1_7',
    'q_1_8', 'q_1_9', 'q_1_10', 'q_1_11', 'q_1_12', 'q_1_13', 'q_2', 'q_3')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1_1 = db.Column(db.Integer)
    q_1_2 = db.Column(db.Integer)
    q_1_3 = db.Column(db.Integer)
    q_1_4 = db.Column(db.Integer)
    q_1_5 = db.Column(db.Integer)
    q_1_6 = db.Column(db.Integer)
    q_1_7 = db.Column(db.Integer)
    q_1_8 = db.Column(db.Integer)
    q_1_9 = db.Column(db.Integer)
    q_1_10 = db.Column(db.Integer)
    q_1_11 = db.Column(db.Integer)
    q_1_12 = db.Column(db.Integer)
    q_1_13 = db.Column(db.Integer)
    q_2 = db.Column(db.Integer)
    q_3 = db.Column(db.Integer)
    
class SSP(db.Model, Export):
    __tablename__ = 'ssp'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9', 'q_10', 'q_11',
    'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20', 'q_21', 'q_22',
    'q_23', 'q_24', 'q_25', 'q_26', 'q_27', 'q_28', 'q_29', 'q_30', 'q_31', 'q_32', 'q_33',
    'q_34', 'q_35', 'q_36', 'q_37', 'q_38', 'q_39', 'q_40', 'q_41', 'q_42', 'q_43', 'q_44',
    'q_45', 'q_46', 'q_47', 'q_48', 'q_49', 'q_50', 'q_51', 'q_52', 'q_53', 'q_54', 'q_55',
    'q_56', 'q_57', 'q_58', 'q_59', 'q_60', 'q_61', 'q_62', 'q_63', 'q_64', 'q_65', 'q_66',
    'q_67', 'q_68', 'q_69', 'q_70', 'q_71', 'q_72', 'q_73', 'q_74', 'q_75', 'q_76', 'q_77',
    'q_78', 'q_79', 'q_80', 'q_81', 'q_82', 'q_83', 'q_84', 'q_85', 'q_86', 'q_87', 'q_88',
    'q_89', 'q_90', 'q_91')
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
    q_58 = db.Column(db.Integer)
    q_59 = db.Column(db.Integer)
    q_60 = db.Column(db.Integer)
    q_61 = db.Column(db.Integer)
    q_62 = db.Column(db.Integer)
    q_63 = db.Column(db.Integer)
    q_64 = db.Column(db.Integer)
    q_65 = db.Column(db.Integer)
    q_66 = db.Column(db.Integer)
    q_67 = db.Column(db.Integer)
    q_68 = db.Column(db.Integer)
    q_69 = db.Column(db.Integer)
    q_70 = db.Column(db.Integer)
    q_71 = db.Column(db.Integer)
    q_72 = db.Column(db.Integer)
    q_73 = db.Column(db.Integer)
    q_74 = db.Column(db.Integer)
    q_75 = db.Column(db.Integer)
    q_76 = db.Column(db.Integer)
    q_77 = db.Column(db.Integer)
    q_78 = db.Column(db.Integer)
    q_79 = db.Column(db.Integer)
    q_80 = db.Column(db.Integer)
    q_81 = db.Column(db.Integer)
    q_82 = db.Column(db.Integer)
    q_83 = db.Column(db.Integer)
    q_84 = db.Column(db.Integer)
    q_85 = db.Column(db.Integer)
    q_86 = db.Column(db.Integer)
    q_87 = db.Column(db.Integer)
    q_88 = db.Column(db.Integer)
    q_89 = db.Column(db.Integer)
    q_90 = db.Column(db.Integer)
    q_91 = db.Column(db.Integer)
    
class PBI(db.Model, Export):
    __tablename__ = 'pbi'
    export_cols = ('p_id', 'status', 'parent', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8',
    'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20',
    'q_21', 'q_22', 'q_23', 'q_24', 'q_25')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    parent = db.Column(db.String(16))
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
    
class CTQ(db.Model, Export):
    __tablename__ = 'ctq'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9', 'q_10', 'q_11',
    'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17', 'q_18', 'q_19', 'q_20', 'q_21', 'q_22', 'q_23', 'q_24', 'q_25',
    'q_26', 'q_27', 'q_28')
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
    
class LES(db.Model, Export):
    __tablename__ = 'les'
    export_cols = ('p_id', 'status', 'event_code', 'event_date', 'property', 'degree', 'duration', 'note')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    event_code = db.Column(db.Integer)
    event_date = db.Column(db.Integer)
    property = db.Column(db.Integer)
    degree = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    note = db.Column(db.Text)

class InOut(db.Model, Export):
    __tablename__ = 'inout'
    export_cols = ('p_id', 'status', 'q_1', 'q_2')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1 = db.Column(db.String(16))
    q_2 = db.Column(db.String(16))
    
class HAMD(db.Model, Export):
    __tablename__ = 'hamd'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8',
    'q_9', 'q_10', 'q_11', 'q_12', 'q_13', 'q_14', 'q_15', 'q_16', 'q_17')
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
    
class YMRS(db.Model, Export):
    __tablename__ = 'ymrs'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7', 'q_8', 'q_9',
    'q_10', 'q_11')
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
    
class CGI(db.Model, Export):
    __tablename__ = 'cgi'
    export_cols = ('p_id', 'status', 'q_1', 'q_2', 'q_3')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1 = db.Column(db.Integer)
    q_2 = db.Column(db.Integer)
    q_3 = db.Column(db.Integer)
    
class BODY_EXAM(db.Model, Export):
    __tablename__ = 'body_exam'
    export_cols = ('p_id', 'status', 'q_1_1', 'q_1_1', 'q_2', 'q_3', 'q_4', 'q_5', 'q_6', 'q_7')
    id = db.Column(db.Integer, primary_key=True)
    p_id = db.Column(db.Integer, db.ForeignKey('patient_infos.id'))
    status = db.Column(db.String(16), db.ForeignKey('follow_ups.status'))
    q_1_1 = db.Column(db.Float)
    q_1_2 = db.Column(db.Float)
    q_2 = db.Column(db.Float)
    q_3 = db.Column(db.Float)
    q_4 = db.Column(db.Float)
    q_5 = db.Column(db.Float)
    q_6 = db.Column(db.Float)
    q_7 = db.Column(db.Float)