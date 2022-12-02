from psycopg.rows import class_row

from app.models.product_model import Product
from db import pool


def get_special_product_random():
    data = []
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Product)) as cursor:
            # for i in range(25):
            sql = """SELECT * FROM public.product ORDER BY random()
                     """

            cursor.execute(sql)
            # data = cursor.fetchone()
            all_special_products = cursor.fetchmany(25)

            for row in all_special_products:
                data.append(dict(row))

            return data
