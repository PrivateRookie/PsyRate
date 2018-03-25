# -*- coding: utf-8 -*-
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import  BadSignature 
from flask import current_app
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    attendaces = db.relationship('User', backref='project', lazy='dynamic')
    
    def generate_invite_code(self, role):
        serialzer = Serializer(current_app.config['SECRET_KEY'], expires_in = 36000)
        token = serialzer.dumps(dict(role=role, project=self.name))
        return token

    def generate_invite_codes(self, role, num):
        with open(role+'_codes.txt', 'w') as f:
            for i in range(num):
                f.write(self.generate_invite_code(role).decode('utf-8')+'\n')
    
    @staticmethod
    def generate_test_project():
        p = Project(name='test_project')
        db.session.add(p)
        db.session.commit()
    

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)
    
    @staticmethod
    def insert_roles():
        roles = {
            'Patient':(Permission.SELFREPORT, True),
            'Doctor':(Permission.SELFREPORT | Permission.OTHERREPORT, False),
            'Moerator':(Permission.SELFREPORT | Permission.OTHERREPORT |
                        Permission.MOERATE_REPORT, False),
            'Administrator':(0xff, False)
                }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
    
class Permission:
    SELFREPORT = 0x01
    OTHERREPORT = 0x02
    MOERATE_REPORT = 0x04
    ADMINISTRATOR = 0x80
                
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    patients = db.relationship('Patient', backref='recorder')
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
        
    @property
    def password(self):
        raise AttributeError('password is not readable')
        
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})
        
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirm = True
        db.session.add(self)
        return True
            
    @staticmethod
    def verify_invite_code(code):
        serialzer = Serializer(current_app.config['SECRET_KEY'])
        try:
            result = serialzer.loads(code)
        except  BadSignature as e:
            return None, None
        role = Role.query.filter_by(name=result['role']).one()
        project = Project.query.filter_by(name=result['project']).one()
        return role, project
            
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
            
class AnonymousUser(AnonymousUserMixin):   
    def can(self, permissions):
        return False
    
login_manager.anonymous_user = AnonymousUser

class Patient(db.Model):
    __tablename__ = 'patient_infos'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(32))
    entry_date = db.Column(db.String(64))
    doctor = db.Column(db.String(32))
    finished = db.Column(db.Boolean, default=False)
    recorder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    def __repr__(self):
        return '<Patient {}>'.format(self.name)
