# -*- coding: utf-8 -*-
import os
from app import create_app, db
from app.models import Role, User
from flask_script import Manager, Shell, Command, Option
from tests.test_db import VirtualFillTestCase
from werkzeug.contrib.fixers import ProxyFix

from app import models, surveymodels

app = create_app(os.getenv('FLASK_CONFIG') or 'dev')
manager = Manager(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

def make_shell_context():
    return dict(app=app, db=db, models=models, surveymodels=surveymodels)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def test(name=None):
    """Run the unit tests."""
    import unittest
    if name is None:
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
    else:       
        suite = unittest.TestSuite()
        suite.addTest(VirtualFillTestCase('test_' + name))
        unittest.TextTestRunner(verbosity=2).run(suite)
        
@manager.command
def init_db():
    """init database"""
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    
    # create adminstator
    ad = User(email='admin@gmail.com', username='admin', password='admin', role_id=4, confirmed=True)
    db.session.add(ad)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
