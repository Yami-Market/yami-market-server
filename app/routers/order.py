# from app.services.special_product_service import get_special_product_random
from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.order_model import NEW_ORDER
from app.services.order_service import get_order_info, insert_info_into_order

bp = Blueprint(name='order', import_name=__name__, url_prefix='/v1')


@bp.get('/order/<string:order_id>')
@jwt_required()
def get_user_order(order_id):

    order_info = get_order_info(order_id)
    # special_products = get_special_product_random()

    app.logger.debug(order_id)
    if order_info is None:
        abort(404, 'order can not be found')

    return jsonify(order_info.dict()), 200


@bp.post('/order')
@jwt_required()
def generate_order():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                order = NEW_ORDER(**body)

                inserted_order_info = insert_info_into_order(
                    order, current_user)
                app.logger.debug(order)

                if inserted_order_info is None:
                    abort(404, 'order can not be found!!!')

                return jsonify(inserted_order_info.dict()), 200
            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)
