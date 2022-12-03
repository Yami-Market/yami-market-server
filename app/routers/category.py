from flask import Blueprint
from flask import current_app as app
from flask import jsonify

from app.services.category_service import get_category_list

bp = Blueprint(name='category', import_name=__name__, url_prefix='/v1')


@bp.get('/category')
def get_category():
    category_list = get_category_list()
    app.logger.debug(category_list)
    return jsonify(category_list.dict()), 200
