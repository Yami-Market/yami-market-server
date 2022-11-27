from enum import Enum

from flask import Blueprint, abort, jsonify, request
from pydantic import BaseModel, ValidationError

bp = Blueprint(name='shopping_cart', import_name=__name__, url_prefix='/v1')


class ShoppingCartType(Enum):
    update = 'update'
    remove = 'remove'


# Model
class ShoppingCart(BaseModel):
    user_id: str
    product_id: str
    quantity: int | None  # optional
    type: ShoppingCartType


@bp.route('/shoppingcart', methods=['GET'])
def get_shopping_cart():
    return jsonify(message='get shopping cart v1'), 200


@bp.route('/shoppingcart', methods=['POST'])
def shopping_cart():
    if request.is_json:
        # read from body
        body = request.get_json()
        if body is not None:
            try:
                shopping_cart = ShoppingCart(**body)
                print(shopping_cart)

                # conn = get_db_connection()
                # cur = conn.cursor()

                # # Update
                # if shopping_cart.type == ShoppingCartType.update:
                #     sql = """select * from public."YAMI_SHOPPING_CART"
                #     where product_id = %s and user_id = %s"""
                #     cur.execute(
                #         sql, (shopping_cart.product_id,
                # shopping_cart.user_id))
                #     data = cur.fetchone()
                #     if data is None:
                #         sql = """insert into public."YAMI_SHOPPING_CART"
                #                     (user_id, product_id, quantity)
                #                     values (%s,%s,%s);
                #             """
                #         cur.execute(sql, (
                #             shopping_cart.user_id,
                #             shopping_cart.product_id,
                #             shopping_cart.quantity,
                #         ))
                #         conn.commit()
                #         cur.close()
                #         conn.close()
                #         return 'success insert'
                #     else:
                #         sql = """ update public."YAMI_SHOPPING_CART"
                #         set quantity = %s
                #         where product_id = %s and user_id = %s
                #         """
                #         cur.execute(
                #             sql,
                #             (shopping_cart.quantity, shopping_cart.product_id,
                #              shopping_cart.user_id))
                #         conn.commit()
                #         cur.close()
                #         conn.close()
                #         return 'success update'

                # # Remove
                # else:
                #     sql = """delete from public."YAMI_SHOPPING_CART"
                #             where product_id = %s and user_id = %s;
                #     """
                #     cur.execute(sql, (
                #         shopping_cart.product_id,
                #         shopping_cart.user_id,
                #     ))
                #     conn.commit()
                #     cur.close()
                #     conn.close()
                #     return 'successful remove'

            except ValidationError as e:
                print(e)
                abort(400, 'JSON data is not correct')
        else:
            abort(400, 'request body is empty')
    else:
        abort(400, 'request body must be JSON')
