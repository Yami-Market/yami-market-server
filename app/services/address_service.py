from psycopg.rows import class_row

from app.models.address_model import Address, AddressBodyParams, AddressList
from app.models.user_model import User
from app.utils.id import nano_id
from db import pool


def get_address_list(user: User, address_type='shipping'):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Address)) as cursor:
            sql = """select * from public.address
                        where user_id = %s and type = %s
                        and deleted = false
                    """

            cursor.execute(sql, (
                user.id,
                address_type,
            ))

            addresses = cursor.fetchall()

            return AddressList(items=addresses)


def create_new_address(user: User,
                       address: AddressBodyParams,
                       address_type='shipping'):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Address)) as cursor:
            address_id = nano_id()

            sql = """insert into public.address
                        (id, user_id, first_name, last_name, street_address,
                         optional_address, city, state, country, zip_code,
                         phone_number, email, type)
                        values (%s, %s, %s, %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s)
                        returning *
                    """

            cursor.execute(sql, (
                address_id,
                user.id,
                address.first_name,
                address.last_name,
                address.street_address,
                address.optional_address,
                address.city,
                address.state,
                address.country,
                address.zip_code,
                address.phone_number,
                address.email,
                address_type,
            ))

            conn.commit()

            return cursor.fetchone()


def update_address(user: User, address_id: str, address: AddressBodyParams):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """update public.address
                        set first_name = %s, last_name = %s,
                            street_address = %s,
                            optional_address = %s, city = %s, state = %s,
                            country = %s, zip_code = %s, phone_number = %s,
                            email = %s, updated_at = now()
                        where id = %s and user_id = %s
                    """

            cursor.execute(sql, (
                address.first_name,
                address.last_name,
                address.street_address,
                address.optional_address,
                address.city,
                address.state,
                address.country,
                address.zip_code,
                address.phone_number,
                address.email,
                address_id,
                user.id,
            ))

            conn.commit()


def delete_address(user: User, address_id: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """update public.address
                        set deleted = true, updated_at = now()
                        where id = %s and user_id = %s
                    """

            cursor.execute(sql, (
                address_id,
                user.id,
            ))

            conn.commit()
