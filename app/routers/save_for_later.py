# /savelater get same sa shopping cart
# /savelater

# delete /savelater/:product_id

# put /savelater/:product_id
# '''
# if product exist in sc, not exist in rl
# remove product in sc, insert product to rl

# elif product not exist in sc, exist in rl
# remove product in rl, add product to sc

# else
# abort 404
# '''
import json

from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required

from app.services.save_later_service import (
    create_user_save_later_product,
    delete_user_save_later_product,
    get_user_save_later,
    get_user_save_later_product,
)
from app.services.shopping_cart_service import (
    create_user_shopping_cart_product_with_quantity,
    delete_user_shopping_cart_product,
    get_user_shopping_cart_product,
)

bp = Blueprint(name='save_later', import_name=__name__, url_prefix='/v1')


@bp.get('/savelater')
@jwt_required()
def get_save_later():
    app.logger.debug(current_user)
    user_save_later = get_user_save_later(current_user)
    return jsonify(json.loads(user_save_later.json())), 200


@bp.delete('/savelater/<string:product_id>')
@jwt_required()
def remove_product_from_save_later(product_id: str):
    app.logger.debug(current_user)
    app.logger.debug(product_id)

    product = get_user_save_later_product(current_user, product_id)

    if product is None:
        abort(404)  # raise Not Found Error

    delete_user_save_later_product(current_user, product_id)
    return Response(status=204)


@bp.put('/savelater/<string:product_id>')
@jwt_required()
def edit_product_to_save_later(product_id: str):
    product_shopping_cart = get_user_shopping_cart_product(
        current_user, product_id)
    product_save_later = get_user_save_later_product(current_user, product_id)

    if product_shopping_cart is not None and product_save_later is None:
        create_user_save_later_product(current_user, product_id)
        delete_user_shopping_cart_product(current_user, product_id)

        return Response(status=201)

    elif product_shopping_cart is None and product_save_later is not None:

        # body = ShoppingCartPutBodyParams(quantity=1)
        # create_user_shopping_cart_product(current_user, product_id, body)

        create_user_shopping_cart_product_with_quantity(
            current_user, product_id, 1)
        delete_user_save_later_product(current_user, product_id)

        return Response(status=201)
    else:
        abort(400)
