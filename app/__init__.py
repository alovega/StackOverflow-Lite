from flask import Flask
from flask_restful import Api
from app.app import Questions
<<<<<<< HEAD
from app.app import Answer

=======
from app.app import Question
>>>>>>> a7d3ab658f6a0d8d749fba37c57afc3841228d30
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
<<<<<<< HEAD
    api.add_resource(Answer, '/answer/<int:id>', endpoint='answers')
=======
    api.add_resource(Question, '/question/<int:id>', endpoint='question')
>>>>>>> a7d3ab658f6a0d8d749fba37c57afc3841228d30
