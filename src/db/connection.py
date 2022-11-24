import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if DB_HOST is None:
    raise ValueError('DB_HOST is not set')
elif DB_NAME is None:
    raise ValueError('DB_NAME is not set')
elif DB_USERNAME is None:
    raise ValueError('DB_USERNAME is not set')
elif DB_PASSWORD is None:
    raise ValueError('DB_PASSWORD is not set')


def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST,
                            database=DB_NAME,
                            user=DB_USERNAME,
                            password=DB_PASSWORD,
                            cursor_factory=psycopg2.extras.RealDictCursor)
    return conn
