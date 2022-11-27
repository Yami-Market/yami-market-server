from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.shopping_cart_model import ShoppingCartBodyParams
from app.services.shopping_cart_service import (
    get_user_shopping_cart,
    update_user_shopping_cart,
)
from app.utils.response_message import ClientErrorMessage

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

                update_user_shopping_cart(current_user, product_id,
                                          shopping_cart_params)

                return jsonify(message='Shopping cart update success'), 200

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400, ClientErrorMessage.empty_json_body)
    else:
        abort(400, ClientErrorMessage.invalid_json_body)


# TODO : Implement delete product from shopping cart
@bp.delete('/shoppingcart/<string:product_id>')
@jwt_required()
def remove_product_from_shopping_cart(product_id: str):
    pass
