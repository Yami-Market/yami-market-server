from psycopg.rows import class_row

from db import pool

from ..models.category_model import Category, CategoryList


def get_category_list():
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Category)) as cursor:
            sql = """select * from public.category_recursive_view
                    """

            cursor.execute(sql)

            categories = cursor.fetchall()

            return CategoryList(items=categories)
