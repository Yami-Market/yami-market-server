from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request

from app.services.category_service import (
    get_all_flatten_category_by_level_1_id,
    get_all_flatten_category_by_level_2_id,
    get_all_flatten_category_by_level_3_id,
    get_category_list,
    get_category_path_by_id,
    get_recursive_category_by_id,
)
from app.services.product_service import get_all_product_by_category_list

bp = Blueprint(name='category', import_name=__name__, url_prefix='/v1')


@bp.get('/category')
def get_category():
    category_list = get_category_list()
    # app.logger.debug(category_list)
    return jsonify(category_list.dict()), 200


@bp.get('/category/<string:category_id>')
def get_all_products_by_category_id(category_id):

    page = request.args.get('page', 1, type=int)

    app.logger.debug(page)

    target_category = get_recursive_category_by_id(category_id)

    if target_category is None:
        abort(404, f'products in category {category_id} can not be found')

    target_category_path = get_category_path_by_id(category_id)
    app.logger.debug(target_category_path)

    flatten_category_list = None

    if target_category.level == 1:
        flatten_category_list = get_all_flatten_category_by_level_1_id(
            category_id)
    elif target_category.level == 2:
        flatten_category_list = get_all_flatten_category_by_level_2_id(
            category_id)
    elif target_category.level == 3:
        flatten_category_list = get_all_flatten_category_by_level_3_id(
            category_id)

    if flatten_category_list is None or target_category_path is None:
        abort(404, f'products in category {category_id} can not be found')

    level_3_ids = [c.level_3_id for c in flatten_category_list.items]

    app.logger.debug(level_3_ids)

    all_products = get_all_product_by_category_list(level_3_ids, 24,
                                                    24 * (page - 1))

    app.logger.debug(all_products)

    if all_products is None:
        empty_product_list = {'total': 0, 'products': []}

        return jsonify(category_id=category_id,
                       category_name=target_category.name,
                       category_level=target_category.level,
                       category_path=target_category_path.dict(),
                       page=page,
                       **empty_product_list), 200

    return jsonify(category_id=category_id,
                   category_name=target_category.name,
                   category_level=target_category.level,
                   category_path=target_category_path.dict(),
                   page=page,
                   **all_products.dict()), 200
