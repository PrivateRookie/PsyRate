# -*- coding: utf-8 -*-
import os
from app import create_app, db, models, surveymodels
from app.models import Project, Role, User
from flask_script import Manager, Shell, Command, Option
from flask_migrate import Migrate, MigrateCommand
from tests.test_db import VirtualFillTestCase
from werkzeug.contrib.fixers import ProxyFix

app = create_app(os.getenv('FLASK_CONFIG') or 'DEV')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
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
    Project.generate_test_project()
    Role.insert_roles()
    
    # create adminstator
    ad = User(email='admin@gmail.com', username='admin', password='admin', role_id=4, project_id=1, confirmed=True)
    db.session.add(ad)
    db.session.commit()
    
@manager.command
def init_product():
    db.drop_all()
    db.creat_all()
    Role.insert_roles()
    default_project = Project(name='默认工程')
    administrator = User(email='admin@gmail.com', username='admin', password='admin', role_id=4, project_id=1, confirmed=True)
    db.session.add(adminstator)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
