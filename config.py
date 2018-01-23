# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_PREFIX = os.environ.get('MAIL_PREFIX')
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_SERVER = os.environ.get('SMTP_SERVER')
    MAIL_PORT = os.environ.get('SMTP_PORT')
    MAIL_USE_SSL = os.environ.get('USE_SSL')
    MIAL_USE_TLS = os.environ.get('USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
    or ('sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))
    
    
class TestConfig(Config):
    DEBUG = True
    MAIL_SERVER = os.environ.get('SMTP_SERVER')
    MAIL_PORT = os.environ.get('SMTP_PORT')
    MAIL_USE_SSL = os.environ.get('USE_SSL')
    MIAL_USE_TLS = os.environ.get('USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
    or ('sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))

config = {'default':DevelopmentConfig,
          'dev':DevelopmentConfig,
          'test':TestConfig}