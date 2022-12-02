from psycopg.rows import class_row

from app.models.product_model import Product
from db import pool


def get_product_by_id(product_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Product)) as cursor:
            sql = """select * from public.product
                        where id = %s
                     """

            cursor.execute(sql, (product_id, ))

            data = cursor.fetchone()

            return data
