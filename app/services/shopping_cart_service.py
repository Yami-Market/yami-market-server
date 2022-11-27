from psycopg.rows import class_row

from app.models.shopping_cart_model import (
    ShoppingCartBodyParams,
    ShoppingCartItem,
    ShoppingCartItemList,
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


# FIXME: Must validate product_id
def update_user_shopping_cart(user: User, product_id: str,
                              shopping_cart_params: ShoppingCartBodyParams):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """select * from public.shopping_cart
                        where product_id = %s and user_id = %s
                     """

            cursor.execute(sql, (product_id, user.id))

            data = cursor.fetchone()

            if data is None:
                sql = """insert into public.shopping_cart
                            (user_id, product_id, quantity)
                            values (%s,%s,%s);
                        """

                cursor.execute(sql, (
                    user.id,
                    product_id,
                    shopping_cart_params.quantity,
                ))
            else:
                sql = """ update public.shopping_cart
                    set quantity = %s
                    where product_id = %s and user_id = %s
                    """

                cursor.execute(
                    sql, (shopping_cart_params.quantity, product_id, user.id))

            conn.commit()
