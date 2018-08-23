from flask import Flask
from flask_restful import Api

from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    create_api(app)
    return app


def create_api(app):

    api = Api(app)