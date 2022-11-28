from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.shopping_cart_model import ShoppingCartBodyParams
from app.services.shopping_cart_service import (
    create_user_shopping_cart_product,
    delete_user_shopping_cart_product,
    get_user_shopping_cart,
    get_user_shopping_cart_product,
    update_user_shopping_cart_product,
)

bp = Blueprint(name='shopping_cart', import_name=__name__, url_prefix='/v1')


@bp.get('/shoppingcart')
@jwt_required()
def get_shopping_cart():
    app.logger.debug(current_user)
    # app.logger.debug(get_jwt_identity())
    # app.logger.debug(get_current_user())
    user_shopping_cart = get_user_shopping_cart(current_user)
    return jsonify(user_shopping_cart.dict()), 200


@bp.put('/shoppingcart/<string:product_id>')
@jwt_required()
def add_product_to_shopping_cart(product_id: str):
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                shopping_cart_params = ShoppingCartBodyParams(**body)

                product = get_user_shopping_cart_product(
                    current_user, product_id)

                if product is None:
                    create_user_shopping_cart_product(current_user, product_id,
                                                      shopping_cart_params)

                    return Response(status=201)

                update_user_shopping_cart_product(current_user, product_id,
                                                  shopping_cart_params)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


# TODO : Implement delete product from shopping cart
@bp.delete('/shoppingcart/<string:product_id>')
@jwt_required()
def remove_product_from_shopping_cart(product_id: str):
    app.logger.debug(current_user)
    app.logger.debug(product_id)
    try:

        product = get_user_shopping_cart_product(current_user, product_id)

        if product is None:

            return Response(status=204)

        delete_user_shopping_cart_product(current_user, product_id)

        return Response(status=200)

    except ValidationError as e:
        return jsonify(e.errors()), 400
