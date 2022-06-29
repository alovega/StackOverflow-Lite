import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    FLASK_ENV = 'development'
    DEBUG = False
    SECRET_KEY=os.getenv('SECRET_KEY')
    SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT')
    # MAIL_SERVER  =  'smtp.gmail.com'
    # MAIL_PORT  = 465
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT=os.getenv('MAIL_PORT2')
    MAIL_USERNAME=os.getenv('MAIL_USERNAME2')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD2')
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI2')
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT=2525
    MAIL_USERNAME=os.getenv('MAIL_USERNAME2')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD2')
    MAIL_DEFAULT_SENDER='kelvin@example.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SECURITY_PASSWORD_SALT=os.getenv('SECURITY_PASSWORD_SALT')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgres://nrwwdvuzruatqi:ca6e6cf414b7b5a539e93d2074d77da001ec754cd166b58df2b241c747e48ced@ec2-54' \
                   '-83-29-34.compute-1.amazonaws.com:5432/d84nv6pknuhjff '
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app_config = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'staging': 'config.StagingConfig',
    'production': 'config.ProductionConfig',
}
