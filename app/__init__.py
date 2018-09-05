from flask import Flask
from flask_restful import Api
from app.app import Questions
from app.app import Question
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    create_api(app)
    return app


def create_api(app):

    api = Api(app)

    api.add_resource(Questions, '/questions', endpoint='questions')
    api.add_resource(Question, '/question/<int:id>', endpoint='question')