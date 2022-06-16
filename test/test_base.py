import unittest
from app import app
from app.models import db, User, Question, Answer, Category, Badge
from app.user import TokenRefresh, UserLogin, UserRegister


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
        self.app.config.from_object('config.TestingConfig')
        self.app.config.from_envvar('APPLICATION_SETTINGS')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.init_app(self.app)
        db.create_all()
        

    def tearDown(self):
        self.app = None
        db.drop_all()
        