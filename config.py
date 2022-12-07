import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config(object):
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')


class DevelopmentConfig(Config):
    DEBUG = True
    CORS_HEADERS = 'Content-Type'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ['cookies']


class ProductionConfig(Config):
    DEBUG = False
    CORS_HEADERS = 'Content-Type'
    # Dangerous to set to False in production!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    JWT_COOKIE_SECURE = False
    JWT_TOKEN_LOCATION = ['cookies']
