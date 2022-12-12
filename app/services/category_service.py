from psycopg.rows import class_row

from app.models.category_model import (
    Category,
    CategoryList,
    CategoryPath,
    ProductAllCategory,
    ProductAllCategoryList,
)
from db import pool


def get_category_list():
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Category)) as cursor:
            sql = """select * from public.category_recursive_view
                    """

            cursor.execute(sql)

            categories = cursor.fetchall()

            return CategoryList(items=categories)


def get_recursive_category_by_id(category_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Category)) as cursor:
            sql = """select * from public.category_recursive_view
                        where id = %s
                    """

            cursor.execute(sql, (category_id, ))

            categories = cursor.fetchone()

            return categories


def get_all_flatten_category_by_level_1_id(level_1_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ProductAllCategory)) as cursor:
            sql = """select * from public.category_flatten_view
                        where level_1_id = %s
                    """

            cursor.execute(sql, (level_1_id, ))

            categories = cursor.fetchall()

            return ProductAllCategoryList(items=categories)


def get_all_flatten_category_by_level_2_id(level_2_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ProductAllCategory)) as cursor:
            sql = """select * from public.category_flatten_view
                        where level_2_id = %s
                    """

            cursor.execute(sql, (level_2_id, ))

            categories = cursor.fetchall()

            return ProductAllCategoryList(items=categories)


def get_all_flatten_category_by_level_3_id(level_3_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ProductAllCategory)) as cursor:
            sql = """select * from public.category_flatten_view
                        where level_3_id = %s
                    """

            cursor.execute(sql, (level_3_id, ))

            categories = cursor.fetchall()

            return ProductAllCategoryList(items=categories)


def get_product_all_category(level_3_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(ProductAllCategory)) as cursor:
            sql = """select * from public.category_flatten_view
                        where level_3_id = %s
                    """

            cursor.execute(sql, (level_3_id, ))

            categories = cursor.fetchone()

            return categories


def get_category_path_by_id(category_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(CategoryPath)) as cursor:
            sql = """select * from public.category_path_view
                        where id = %s
                    """

            cursor.execute(sql, (category_id, ))

            category = cursor.fetchone()

            return category
