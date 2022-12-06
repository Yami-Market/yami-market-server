from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify

from app.services.product_service import get_product_by_id
from app.services.special_product_service import get_special_product_random

bp = Blueprint(name='product', import_name=__name__, url_prefix='/v1')


@bp.get('/product/<string:product_id>')
def get_product(product_id):
    app.logger.debug(product_id)

    product = get_product_by_id(product_id)

    app.logger.debug(product)

    if product is None:
        abort(404, f'product {product_id} can not be found')

    random_product = get_special_product_random(6)
    random_image_urls = [p.image_url for p in random_product.items]

    return jsonify(product_detail=product.dict(),
                   image_urls=random_image_urls), 200
