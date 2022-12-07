from psycopg.rows import class_row

from app.models.shopping_cart_model import (
    ShoppingCartItem,
    ShoppingCartItemList,
    ShoppingCartPostBodyParams,
    ShoppingCartPutBodyParams,
)
from app.models.user_model import User
from db import pool


def get_user_shopping_cart(user: User):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ShoppingCartItem)) as cursor:
            sql = """select * from public.shopping_cart
                        where user_id = %s
                    """

            cursor.execute(sql, (user.id, ))

            shopping_cart = cursor.fetchall()

            return ShoppingCartItemList(items=shopping_cart)


def get_user_shopping_cart_product(user: User, product_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ShoppingCartItem)) as cursor:
            sql = """select * from public.shopping_cart
                        where product_id = %s and user_id = %s
                     """

            cursor.execute(sql, (
                product_id,
                user.id,
            ))

            data = cursor.fetchone()

            return data


def create_user_shopping_cart_product(
        user: User, product_id: str,
        shopping_cart_params: ShoppingCartPutBodyParams):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """insert into public.shopping_cart
                        (user_id, product_id, quantity)
                        values (%s,%s,%s);
                    """

            cursor.execute(sql, (
                user.id,
                product_id,
                shopping_cart_params.quantity,
            ))

            conn.commit()


def upsert_user_entire_shopping_cart(
        user: User, shopping_cart_params: ShoppingCartPostBodyParams):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """insert into public.shopping_cart
                        (user_id, product_id, quantity)
                        values (%s,%s,%s) on conflict (user_id, product_id)
                        do update set quantity = excluded.quantity;
                    """
            print(((
                user.id,
                product.product_id,
                product.quantity,
            ) for product in shopping_cart_params.items))
            cursor.executemany(sql, ((
                user.id,
                product.product_id,
                product.quantity,
            ) for product in shopping_cart_params.items))

            conn.commit()


def update_user_shopping_cart_product(
        user: User, product_id: str,
        shopping_cart_params: ShoppingCartPutBodyParams):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """update public.shopping_cart
                        set quantity = %s
                        where product_id = %s and user_id = %s;
                    """

            cursor.execute(sql, (
                shopping_cart_params.quantity,
                product_id,
                user.id,
            ))

            conn.commit()


def delete_user_shopping_cart_product(user: User, product_id: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """delete from public.shopping_cart
                        where product_id = %s and user_id = %s;
                    """

            cursor.execute(sql, (
                product_id,
                user.id,
            ))

            conn.commit()
