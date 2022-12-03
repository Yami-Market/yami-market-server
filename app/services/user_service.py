from psycopg.rows import class_row
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user_model import NewUser, User, User_Profile
from app.utils.id import nano_id
from db import pool


def hash_password(password: str):
    return generate_password_hash(password)


def check_password(hashed_password: str, password: str):
    return check_password_hash(hashed_password, password)


def get_user_by_email(email: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(User)) as cursor:
            sql = """select * from public.user
                        where email = %s
                    """

            cursor.execute(sql, (email, ))

            user = cursor.fetchone()

            return user


def create_new_user(new_user: NewUser):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
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


def get_user_profile(user: User_Profile):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(User_Profile)) as cursor:
            sql = """select id, email, first_name, last_name, gender
                        from public.user
                        where id = %s
                    """

            cursor.execute(sql, (user.id, ))

            # data = cursor.fetchone()
            # data = User_Profle(**data)
            user_profile = cursor.fetchone()

            return user_profile
