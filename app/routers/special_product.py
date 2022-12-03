from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify

from app.services.special_product_service import get_special_product_random

bp = Blueprint(name='special_product', import_name=__name__, url_prefix='/v1')


@bp.get('/special/limited')
def get_limited_edition_product():
    special_products = get_special_product_random()
    app.logger.debug(special_products)

    if special_products is None:
        abort(404, 'No Limited Edition Product for now')
    return jsonify(special_products.dict()), 200


@bp.get('/special/best')
def get_best_sellers_product():
    special_products = get_special_product_random()
    app.logger.debug(special_products)

    if special_products is None:
        abort(404, 'No Best Sellers Product for now')
    return jsonify(special_products.dict()), 200


@bp.get('/special/fast')
def get_selling_fast_product():
    special_products = get_special_product_random()
    app.logger.debug(special_products)

    if special_products is None:
        abort(404, 'No Selling Fast Product for now')
    return jsonify(special_products.dict()), 200
