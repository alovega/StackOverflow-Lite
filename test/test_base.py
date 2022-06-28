import os
import unittest
from app import app, mail
from app.models import db, User, Question, Answer, Category, Badge
from app.token import *
from app.user import *


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['FLASK_ENV'] = 'testing'
        self.app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
        self.app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
        self.app.config.from_object('config.TestingConfig')
        self.app.config.from_envvar('APPLICATION_SETTINGS')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        mail.init_app(self.app)
        self.app_context.push()
        db.init_app(self.app)
        db.create_all()
        

    def tearDown(self):
        self.app = None
        db.drop_all()
        