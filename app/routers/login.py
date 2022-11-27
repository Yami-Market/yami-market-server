from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import create_access_token
from pydantic import ValidationError

from app.models.user_model import UserBodyParams
from app.services.user_service import check_password, get_user_by_email
from app.utils.response_message import ClientErrorMessage

bp = Blueprint(name='login', import_name=__name__, url_prefix='/v1')


@bp.route('/login', methods=['POST'])
def login():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                user_params = UserBodyParams(**body)
                print(user_params)

                exist_user = get_user_by_email(user_params.email)

                if exist_user is None or not check_password(
                        exist_user.password, user_params.password):
                    return abort(401,
                                 ClientErrorMessage.wrong_email_or_password)

                access_token = create_access_token(identity=user_params)
                return jsonify(access_token=access_token)

            except ValidationError as e:
                return jsonify(e.errors()), 400

        else:
            abort(400, ClientErrorMessage.empty_json_body)
    else:
        abort(400, ClientErrorMessage.invalid_json_body)
