from psycopg.rows import class_row

from app.models.order_model import (
    NewOrderProduct,
    Order,
    OrderProductDetail,
    OrderProductDetailList,
)
from app.models.user_model import User
from app.utils.id import nano_id
from db import pool


def get_order(user: User, order_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(OrderProductDetail)) as cursor:
            sql = """select
                            id,
                            order_date,
                            ship_date,
                            payment_date,
                            shipping_fee,
                            tax_rate,
                            user_id,
                            credit_card_id,
                            shipping_address_id,
                            subtotal_price,
                            products,
                            shipping_address,
                            credit_card
                        from public.order
                        inner join
                        (select t.order_id as order_id,
                            sum(t.unit_price * t.order_quantity)
                                                as subtotal_price,
                            json_agg(row_to_json(t)) as products
                        from (
                            select public.order.id as order_id,
                                    unit_price, order_quantity,
                                    p.*
                            from public.order
                            inner join
                                public.order_detail od
                                    on public.order.id = od.order_id
                            inner join
                                public.product p on p.id = od.product_id
                            where user_id = %s and public.order.id = %s
                            ) as t
                        group by t.order_id) as pt
                        on pt.order_id = public.order.id

                        inner join
                        (select id as address_id,
                                    row_to_json(t) as shipping_address
                            from (select *
                                    from address
                                    where user_id = %s) as t) as a
                        on public.order.shipping_address_id = a.address_id

                        inner join
                        (select id as c_id,
                                row_to_json(t) as credit_card
                            from (select *
                                    from credit_card
                                    where user_id = %s) as t) as c
                        on public.order.credit_card_id = c.c_id
                """

            cursor.execute(sql, (
                user.id,
                order_id,
                user.id,
                user.id,
            ))

            order = cursor.fetchone()

            return order


def get_order_list(user: User):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(OrderProductDetail)) as cursor:
            sql = """select
                            id,
                            order_date,
                            ship_date,
                            payment_date,
                            shipping_fee,
                            tax_rate,
                            user_id,
                            credit_card_id,
                            shipping_address_id,
                            subtotal_price,
                            products,
                            shipping_address,
                            credit_card
                        from public.order
                        inner join
                        (select t.order_id as order_id,
                            sum(t.unit_price * t.order_quantity)
                                                as subtotal_price,
                            json_agg(row_to_json(t)) as products
                        from (
                            select public.order.id as order_id,
                                    unit_price, order_quantity,
                                    p.*
                            from public.order
                            inner join
                                public.order_detail od
                                    on public.order.id = od.order_id
                            inner join
                                public.product p on p.id = od.product_id
                            where user_id = %s
                            ) as t
                        group by t.order_id) as pt
                    on pt.order_id = public.order.id

                    inner join
                        (select id as address_id,
                                    row_to_json(t) as shipping_address
                            from (select *
                                    from address
                                    where user_id = %s) as t) as a
                        on public.order.shipping_address_id = a.address_id

                        inner join
                        (select id as c_id,
                                row_to_json(t) as credit_card
                            from (select *
                                    from credit_card
                                    where user_id = %s) as t) as c
                        on public.order.credit_card_id = c.c_id
                """

            cursor.execute(sql, (
                user.id,
                user.id,
                user.id,
            ))

            orders = cursor.fetchall()

            return OrderProductDetailList(items=orders)


def create_new_order(user: User, shipping_fee: float, tax_rate: float,
                     credit_card_id: str, shipping_address_id: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Order)) as cursor:
            order_id = nano_id()

            sql = """insert into public.order
                        (id, shipping_fee, tax_rate, user_id,
                        credit_card_id, shipping_address_id)
                        values (%s, %s, %s, %s, %s, %s)
                        returning *
                    """

            cursor.execute(sql, (
                order_id,
                shipping_fee,
                tax_rate,
                user.id,
                credit_card_id,
                shipping_address_id,
            ))

            conn.commit()

            return cursor.fetchone()


def create_new_order_detail(order_id, products: list[NewOrderProduct]):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            sql = """insert into public.order_detail
                        (order_id, product_id, unit_price, order_quantity)
                        values (%s, %s, %s, %s)
                    """

            cursor.executemany(sql, ((
                order_id,
                product.product_id,
                product.list_price,
                product.quantity,
            ) for product in products))

            conn.commit()
