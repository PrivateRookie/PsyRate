# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_PREFIX = os.environ.get('MAIL_PREFIX')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_SERVER = os.environ.get('SMTP_SERVER')
    MAIL_PORT = os.environ.get('SMTP_PORT')
    MAIL_USE_SSL = os.environ.get('USE_SSL')
    MIAL_USE_TLS = os.environ.get('USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass
        
class ProductConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SERVER_NAME=os.environ.get('SERVER_NAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URL') \
    or ('sqlite:///' + os.path.join(basedir, 'data-pro.sqlite'))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
    or ('sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))
    
    
class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
    or ('sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))

config = {'DEFAULT':DevelopmentConfig,
          'DEV':DevelopmentConfig,
          'PRODUCT':ProductConfig,
          'TEST':TestConfig}