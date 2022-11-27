import os

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')


class DevelopmentConfig(Config):
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = False


class ProductionConfig(Config):
    DEBUG = False
    # Dangerous to set to False in production!
    JWT_ACCESS_TOKEN_EXPIRES = False
    # from datetime import timedelta
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
