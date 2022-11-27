import os

from dotenv import load_dotenv

from db import create_db_connection_pool

load_dotenv()


class Config(object):
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    DB_POOL = create_db_connection_pool(DB_HOST, DB_NAME, DB_USERNAME,
                                        DB_PASSWORD)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
