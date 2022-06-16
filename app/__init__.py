from flask import Flask
from flask_restful import Api
import os
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from .models import *
from .schema import ma
# from app.templates import TEMPLATE
from .user import UserRegister, UserLogin, TokenRefresh
from config import app_config

import logging

logging.basicConfig(filename = 'app.log', level=logging.ERROR, format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s')

def create_api(app):

    api = Api(app)

    # api.add_resource(Questions, '/questions', endpoint='questions')
    # api.add_resource(Question, '/questions/<int:id>', endpoint='question')
    # api.add_resource(Answers, '/questions/<int:id>/answers', endpoint='answers')
    # api.add_resource(Answer, '/questions/<int:id>/answers/<int:answer_id>', endpoint='answer')
    api.add_resource(UserRegister, '/auth/signup', endpoint='Register')
    api.add_resource(UserLogin, '/auth/login', endpoint='Login')
    api.add_resource(TokenRefresh, '/auth/login/refresh', endpoint='Refresh')


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config.from_object(app_config.get(os.environ.get('APP_SETTINGS')))
app.config.from_envvar('APPLICATION_SETTINGS')
# Swagger(app, template=TEMPLATE)
jwt = JWTManager(app)
db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)
from .models import Answer, User, Question, Category, Badge
api = Api(app)
api.add_resource(UserRegister, '/auth/signup', endpoint='Register')
api.add_resource(UserLogin, '/auth/login', endpoint='Login')
api.add_resource(TokenRefresh, '/auth/login/refresh', endpoint='Refresh')

# create_api(app)




