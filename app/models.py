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
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))