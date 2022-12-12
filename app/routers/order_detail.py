from flask import Blueprint, jsonify

bp = Blueprint(name='order_detail', import_name=__name__, url_prefix='/v1')


@bp.post('/order_detail/<string:order_id>')
# @jwt_required()
def get_order_detail(order_id):

    return jsonify(message='Hey')
