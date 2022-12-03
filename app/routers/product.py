from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify

from app.services.product_service import get_product_by_id

bp = Blueprint(name='product', import_name=__name__, url_prefix='/v1')


@bp.get('/product/<string:product_id>')
def get_product(product_id):
    app.logger.debug(product_id)

    product = get_product_by_id(product_id)

    app.logger.debug(product)

    if product is None:
        abort(404, f'product {product_id} can not be found')

    return jsonify(product.dict()), 200
