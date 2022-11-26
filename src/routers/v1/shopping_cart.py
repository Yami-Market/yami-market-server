from enum import Enum

from flask import Blueprint, abort, jsonify, request
from pydantic import BaseModel, ValidationError

from db.connection import get_db_connection

shopping_cart = Blueprint(name='shopping_cart',
                          import_name=__name__,
                          url_prefix='/v1/shoppingcart')


class ShoppingCartType(Enum):
    update = 'update'
    remove = 'remove'


# model
class ShoppingCart(BaseModel):
    user_id: str
    product_id: str
    quantity: int | None  # optional
    type: ShoppingCartType


@shopping_cart.route('', methods=['GET'])
def get_shopping_cart_v1():
    return jsonify(message='get shopping cart v1'), 200


@shopping_cart.route('', methods=['POST'])
def v1_shoppingcart():
    if request.is_json:  # read from body
        body = request.get_json()
        if body is not None:
            try:
                shopping_cart = ShoppingCart(**body)
                print(shopping_cart)

                conn = get_db_connection()
                cur = conn.cursor()

                # Update
                if shopping_cart.type == ShoppingCartType.update:
                    sql = """select * from public."YAMI_SHOPPING_CART"
                    where product_id = %s and user_id = %s"""
                    cur.execute(
                        sql, (shopping_cart.product_id, shopping_cart.user_id))
                    data = cur.fetchone()
                    if data is None:
                        sql = """insert into public."YAMI_SHOPPING_CART"
                                    (user_id, product_id, quantity)
                                    values (%s,%s,%s);
                            """
                        cur.execute(sql, (
                            shopping_cart.user_id,
                            shopping_cart.product_id,
                            shopping_cart.quantity,
                        ))
                        conn.commit()
                        cur.close()
                        conn.close()
                        return 'success insert'
                    else:
                        sql = """ update public."YAMI_SHOPPING_CART"
                        set quantity = %s
                        where product_id = %s and user_id = %s
                        """
                        cur.execute(
                            sql,
                            (shopping_cart.quantity, shopping_cart.product_id,
                             shopping_cart.user_id))
                        conn.commit()
                        cur.close()
                        conn.close()
                        return 'success update'

                # Remove
                else:
                    sql = """delete from public."YAMI_SHOPPING_CART"
                            where product_id = %s and user_id = %s;
                    """
                    cur.execute(sql, (
                        shopping_cart.product_id,
                        shopping_cart.user_id,
                    ))
                    conn.commit()
                    cur.close()
                    conn.close()
                    return 'successful remove'

            except ValidationError:
                return {'message': 'JSON data is not correct'}, 400
            except Exception as e:
                print(e)
                return {'message': 'Something is wrong'}, 500
        else:
            return {'message': 'request body is empty'}, 400
    else:
        abort(400, 'request body must be JSON')
