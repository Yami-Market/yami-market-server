from psycopg.rows import class_row

from app.models.product_model import Product, ProductList
from db import pool


def get_special_product_random(number: int = 25):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Product)) as cursor:
            sql = """SELECT * FROM public.product ORDER BY random()
                     """

            cursor.execute(sql)
            all_special_products = cursor.fetchmany(number)

            return ProductList(items=all_special_products)
