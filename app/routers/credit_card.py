from flask import Blueprint, jsonify
from flask_jwt_extended import current_user, jwt_required

from app.services.credit_card_service import get_credit_card_list

bp = Blueprint(name='credit_card', import_name=__name__, url_prefix='/v1')


@bp.get('/creditcard')
@jwt_required()
def get_credit_card():
    user_credit_card_list = get_credit_card_list(current_user)

    return jsonify(user_credit_card_list.dict()), 200
