from psycopg.rows import class_row
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user_model import NewUser, UpdateUserProfile, User, UserProfile
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


def get_user_profile(user: UserProfile):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(UserProfile)) as cursor:
            sql = """select id, email, first_name, last_name, gender
                        from public.user
                        where id = %s
                    """

            cursor.execute(sql, (user.id, ))

            # data = cursor.fetchone()
            # data = User_Profile(**data)
            user_profile = cursor.fetchone()

            return user_profile


def get_user_by_id(id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(User)) as cursor:
            sql = """select * from public.user
                        where id = %s
                    """

            cursor.execute(sql, (id, ))

            user_profile = cursor.fetchone()

            return user_profile


def update_user_password(user: User, new_password):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            hashed_password = hash_password(new_password)  # type:ignore
            sql = """update public.user
                    set password = %s
                        where id = %s
                    """

            cursor.execute(sql, (
                hashed_password,
                user.id,
            ))

            conn.commit()


def update_user_profile(user: UpdateUserProfile, id: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """update public.user
                    set first_name = %s, last_name = %s, gender = %s
                    where id = %s
                    """

            cursor.execute(sql, (
                user.first_name,
                user.last_name,
                user.gender,
                id,
            ))

            conn.commit()
