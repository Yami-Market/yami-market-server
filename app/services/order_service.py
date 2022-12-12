from datetime import datetime, timezone

from psycopg.rows import class_row

from app.models.order_model import NEW_ORDER, Order
from app.models.user_model import User
from app.utils.id import nano_id
from db import pool


def get_order_info(order_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Order)) as cursor:
            sql = """select * from public.order
                        where id = %s
                     """

            cursor.execute(sql, (order_id, ))

            data = cursor.fetchone()

            return data


def insert_info_into_order(new_order: NEW_ORDER, user: User):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Order)) as cursor:
            order_id = nano_id()

            sql = """insert into public.order
                        (id, order_date, ship_date, payment_date, shipping_fee,
                        tax_rate, user_id, credit_card_id, shipping_address_id)
                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s);
                    """

            cursor.execute(sql, (
                order_id,
                datetime.now(timezone.utc),
                None,
                None,
                new_order.shipping_fee,
                new_order.tax_rate,
                user.id,
                new_order.credit_card_id,
                new_order.shipping_address_id,
            ))

            conn.commit()

            extract_info = """select * from public.order
                        where id = %s
                     """
            cursor.execute(extract_info, (order_id, ))

            data = cursor.fetchone()

            return data
