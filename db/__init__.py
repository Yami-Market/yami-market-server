import psycopg2
import psycopg2.extras
import psycopg2.pool


def create_db_connection_pool(host: str | None,
                              database: str | None,
                              user: str | None,
                              password: str | None,
                              *,
                              minconn=1,
                              maxconn=20):

    if host is None:
        raise ValueError('db host is not set')
    elif database is None:
        raise ValueError('db name is not set')
    elif user is None:
        raise ValueError('db username is not set')
    elif password is None:
        raise ValueError('db password is not set')

    pool = psycopg2.pool.SimpleConnectionPool(
        minconn=minconn,
        maxconn=maxconn,
        host=host,
        database=database,
        user=user,
        password=password,
        cursor_factory=psycopg2.extras.RealDictCursor)

    return pool
