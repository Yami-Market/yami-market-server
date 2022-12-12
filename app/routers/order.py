import json

from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.order_model import NewOrderBodyParams
from app.services.order_service import (
    create_new_order,
    create_new_order_detail,
    get_order,
    get_order_list,
)

bp = Blueprint(name='order', import_name=__name__, url_prefix='/v1')


@bp.get('/order/<string:order_id>')
@jwt_required()
def get_user_order(order_id):
    order = get_order(current_user, order_id)

    if order is None:
        abort(404)

    return jsonify(json.loads(order.json())), 200


@bp.get('/order')
@jwt_required()
def get_user_order_list():
    orders = get_order_list(current_user)

    if orders is None:
        abort(404)

    # app.logger.debug(orders)

    return jsonify(json.loads(orders.json())), 200


@bp.post('/order')
@jwt_required()
def create_user_order():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:

                order_params = NewOrderBodyParams(**body)
                tax_rate = 0.1
                new_order = create_new_order(current_user,
                                             order_params.shipping_fee,
                                             tax_rate,
                                             order_params.credit_card_id,
                                             order_params.shipping_address_id)

                if new_order is None:
                    abort(500)

                app.logger.debug(new_order)

                create_new_order_detail(new_order.id, order_params.products)

                return jsonify(json.loads(new_order.json())), 201

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)
