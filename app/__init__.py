from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.app import Question, Answer
from app.app import Questions,Answers
from app.user import UserRegister, UserLogin, TokenRefresh

from instance.config import app_config

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)
    create_api(app)
    return app


def create_api(app):

    api = Api(app)

    api.add_resource(Questions, '/questions', endpoint='questions')
    api.add_resource(Question, '/question/<int:id>', endpoint='question')
    api.add_resource(Answers,'/questions/<int:id>/answers', endpoint='answers')
    api.add_resource(Answer,'/questions/<int:id>/answers/<int:answer_id>', endpoint='answer')
    api.add_resource(UserRegister,'/auth/signup', endpoint='Register')
    api.add_resource(UserLogin, '/auth/login', endpoint='Login')
    api.add_resource(TokenRefresh, '/auth/login/refresh', endpoint='Refresh')
