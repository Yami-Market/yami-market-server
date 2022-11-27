from werkzeug.security import check_password_hash, generate_password_hash

from app import get_db_conn
from app.models.user import NewUser
from app.utils.id import nano_id


def hash_password(password: str):
    return generate_password_hash(password)


def check_password(hashed_password: str, password: str):
    return check_password_hash(hashed_password, password)


def get_user_by_email(email: str):
    conn = get_db_conn()

    cursor = conn.cursor()

    sql = """select * from public.user
    where email = %s"""

    cursor.execute(sql, (email, ))

    user = cursor.fetchone()
    cursor.close()

    return user


def create_new_user(new_user: NewUser):
    conn = get_db_conn()

    cursor = conn.cursor()

    user_id = nano_id()
    hashed_password = hash_password(new_user.password)

    sql = """insert into public.user
                (id, email, password)
                values (%s,%s,%s);
            """

    cursor.execute(sql, (
        user_id,
        new_user.email,
        hashed_password,
    ))

    conn.commit()
    cursor.close()
