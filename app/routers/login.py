from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import create_access_token, set_access_cookies
from pydantic import ValidationError

from app.models.user_model import UserBodyParams
from app.services.user_service import check_password, get_user_by_email
from app.utils.response_message import ClientErrorMessage

bp = Blueprint(name='login', import_name=__name__, url_prefix='/v1')


@bp.post('/login')
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

                response = jsonify(message='login successful',
                                   user={
                                       'id': exist_user.id,
                                       'email': exist_user.email,
                                       'first_name': exist_user.first_name,
                                       'last_name': exist_user.last_name,
                                       'gender': exist_user.gender
                                   })
                access_token = create_access_token(identity=user_params)
                set_access_cookies(response, access_token)
                return response
                # return jsonify(access_token=access_token)

            except ValidationError as e:
                return jsonify(e.errors()), 400

        else:
            abort(400)
    else:
        abort(415)
