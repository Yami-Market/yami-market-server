from psycopg.rows import class_row

from app.models.save_later_model import (
    SaveLater,
    SaveLaterItemProductList,
    SaveLaterProduct,
)
from app.models.user_model import User
from db import pool


def get_user_save_later(user: User):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(SaveLaterProduct)) as cursor:
            sql = """select product_id, name, list_price, image_url,
                        category_id, created_at
                          from public.save_later sl
                        inner join public.product p on sl.product_id = p.id
                        where user_id = %s
                    """

            cursor.execute(sql, (user.id, ))

            save_later = cursor.fetchall()

            return SaveLaterItemProductList(items=save_later)


def get_user_save_later_product(user: User, product_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(SaveLater)) as cursor:
            sql = """select * from public.save_later
                        where product_id = %s and user_id = %s
                     """

            cursor.execute(sql, (
                product_id,
                user.id,
            ))

            data = cursor.fetchone()

            return data


def delete_user_save_later_product(user: User, product_id: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """delete from public.save_later
                        where product_id = %s and user_id = %s;
                    """

            cursor.execute(sql, (
                product_id,
                user.id,
            ))

            conn.commit()


def create_user_save_later_product(user: User, product_id: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """insert into public.save_later
                        (user_id, product_id)
                        values (%s,%s);
                    """

            cursor.execute(sql, (
                user.id,
                product_id,
            ))

            conn.commit()
