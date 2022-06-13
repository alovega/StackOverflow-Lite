import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    DATABASE_URL = "dbname='postgres' user='root' host='localhost' password='root'"


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DATABASE_URL = "dbname='test_db' user='root' host='localhost' password='root'"
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    DATABASE_URL = 'postgres://nrwwdvuzruatqi:ca6e6cf414b7b5a539e93d2074d77da001ec754cd166b58df2b241c747e48ced@ec2-54' \
                   '-83-29-34.compute-1.amazonaws.com:5432/d84nv6pknuhjff '


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
