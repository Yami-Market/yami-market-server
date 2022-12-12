from psycopg.rows import class_row

from app.models.credit_card_model import (
    CreditCard,
    CreditCardList,
    NewCreditCardBody,
)
from app.models.user_model import User
from app.utils.id import nano_id
from db import pool


def get_credit_card_list(user: User):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(CreditCard)) as cursor:
            sql = """select * from public.credit_card
                        where user_id = %s and deleted = false
                    """

            cursor.execute(sql, (user.id, ))

            credit_cards = cursor.fetchall()

            return CreditCardList(items=credit_cards)


def get_credit_card(user: User, credit_card_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(CreditCard)) as cursor:
            sql = """select * from public.credit_card
                        where user_id = %s and id = %s and deleted = false
                    """

            cursor.execute(sql, (
                user.id,
                credit_card_id,
            ))

            credit_card = cursor.fetchone()

            return credit_card


def create_credit_card(user: User, billing_address_id: str,
                       credit_card: NewCreditCardBody):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            credit_card_id = nano_id()

            sql = """insert into public.credit_card
                        (id, user_id, billing_address_id, card_type,
                         card_number, card_holder_name, card_expiry_month,
                         card_expiry_year, cvv_code)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

            cursor.execute(sql, (
                credit_card_id,
                user.id,
                billing_address_id,
                credit_card.card_type,
                credit_card.card_number,
                credit_card.card_holder_name,
                credit_card.card_expiry_month,
                credit_card.card_expiry_year,
                credit_card.cvv_code,
            ))

            conn.commit()


def delete_credit_card(user: User, credit_card_id: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """update public.credit_card
                        set deleted = true, updated_at = now()
                        where id = %s and user_id = %s
                    """

            cursor.execute(sql, (
                credit_card_id,
                user.id,
            ))

            conn.commit()
