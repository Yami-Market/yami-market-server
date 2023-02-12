import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = os.getenv('DB_PORT', 5432)
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL is None:
    if DB_HOST is None:
        raise ValueError('DB_HOST is not set')
    if DB_NAME is None:
        raise ValueError('DB_NAME is not set')
    if DB_USERNAME is None:
        raise ValueError('DB_USERNAME is not set')
    if DB_PASSWORD is None:
        raise ValueError('DB_PASSWORD is not set')

pool = ConnectionPool(
    DATABASE_URL or
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    min_size=1,
    max_size=20,
)
