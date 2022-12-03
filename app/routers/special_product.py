from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify

from app.services.special_product_service import get_special_product_random

bp = Blueprint(name='special_product', import_name=__name__, url_prefix='/v1')


@bp.get('/special_product/limited_edition')
def get_limited_edition_product():
    special_products = get_special_product_random()
    app.logger.debug(special_products)

    if special_products is None:
        abort(404, 'No Special Product for now')
    return jsonify(special_products), 200


@bp.get('/special_product/best_sellers')
def get_best_sellers_product():
    special_products = get_special_product_random()
    app.logger.debug(special_products)

    if special_products is None:
        abort(404, 'No Special Product for now')
    return jsonify(special_products), 200


@bp.get('/special_product/selling_fast')
def get_selling_fast_product():
    special_products = get_special_product_random()
    app.logger.debug(special_products)

    if special_products is None:
        abort(404, 'No Special Product for now')
    return jsonify(special_products), 200


# /v1/p/best
"""
 [{
        id,name,....
    },{
        id,name,....
    },{
        id,name,....
    }]
"""

# /v1/p/limited
"""
 [{
        id,name,....
    },{
        id,name,....
    },{
        id,name,....
    }]
"""

# /v1/p/fast
"""
 [{
        id,name,....
    },{
        id,name,....
    },{
        id,name,....
    }]
"""
