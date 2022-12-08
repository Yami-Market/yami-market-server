from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.shopping_cart_model import (
    ShoppingCartPostBodyParams,
    ShoppingCartPutBodyParams,
)
from app.services.shopping_cart_service import (
    create_user_shopping_cart_product,
    delete_user_shopping_cart_product,
    get_user_shopping_cart_product,
    get_user_shopping_cart_product_detail_list,
    update_user_shopping_cart_product,
    upsert_user_entire_shopping_cart,
)

bp = Blueprint(name='shopping_cart', import_name=__name__, url_prefix='/v1')


@bp.get('/shoppingcart')
@jwt_required()
def get_shopping_cart():
    # app.logger.debug(current_user)
    # app.logger.debug(get_jwt_identity())
    # app.logger.debug(get_current_user())
    user_shopping_cart = get_user_shopping_cart_product_detail_list(
        current_user)
    return jsonify(user_shopping_cart.dict()), 200


@bp.post('/shoppingcart')
@jwt_required()
def add_entire_products_to_shopping_cart():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                shopping_cart_params = ShoppingCartPostBodyParams(**body)

                app.logger.debug(shopping_cart_params)

                upsert_user_entire_shopping_cart(current_user,
                                                 shopping_cart_params)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.put('/shoppingcart/<string:product_id>')
@jwt_required()
def add_product_to_shopping_cart(product_id: str):
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                # FIXME: Must validate product_id

                shopping_cart_params = ShoppingCartPutBodyParams(**body)

                product = get_user_shopping_cart_product(
                    current_user, product_id)

                if product is None:
                    create_user_shopping_cart_product(current_user, product_id,
                                                      shopping_cart_params)

                    return Response(status=204)

                update_user_shopping_cart_product(current_user, product_id,
                                                  shopping_cart_params)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.delete('/shoppingcart/<string:product_id>')
@jwt_required()
def remove_product_from_shopping_cart(product_id: str):
    app.logger.debug(current_user)
    app.logger.debug(product_id)

    product = get_user_shopping_cart_product(current_user, product_id)

    if product is None:
        abort(404)  # rasie Not Found Error

    delete_user_shopping_cart_product(current_user, product_id)

    # Response(status=204)
    # jsonify(message='Delete successfully'), 200  # return message
    # abort(400)  #(only for 4/5++ http code) raise error, except error in js,
    # throw error, catch error

    return Response(status=204)
