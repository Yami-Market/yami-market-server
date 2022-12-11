from psycopg.rows import class_row

from app.models.product_model import Product, ProductPagination
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


def get_all_product_by_category_list(category_list: list, limit: int,
                                     offset: int):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ProductPagination)) as cursor:
            sql = """select
                        (
                        select count(*) from public.product
                        where category_id = any(%s)
                        ) as total,
                        (
                            select json_agg(row_to_json(t))
                            from (
                                select * from public.product
                                where category_id = any(%s)
                                order by id
                                limit %s
                                offset %s
                                ) as t
                            ) as products
                     """

            cursor.execute(sql, (
                category_list,
                category_list,
                limit,
                offset,
            ))

            data = cursor.fetchone()

            return data
