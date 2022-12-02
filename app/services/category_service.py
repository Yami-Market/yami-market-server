from psycopg.rows import class_row

from app.models.category_model import Category, CategoryList
from db import pool


def get_category_list():
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Category)) as cursor:
            sql = """select * from public.category_recursive_view
                    """

            cursor.execute(sql)

            categories = cursor.fetchall()

            return CategoryList(items=categories)
