from psycopg.rows import class_row

from app.models.credit_card_model import CreditCard, CreditCardList
from app.models.user_model import User
from db import pool


def get_credit_card_list(user: User):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(CreditCard)) as cursor:
            sql = """select * from public.credit_card
                        where user_id = %s
                    """

            cursor.execute(sql, (user.id, ))

            credit_cards = cursor.fetchall()

            return CreditCardList(items=credit_cards)
