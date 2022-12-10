from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError
from werkzeug.security import check_password_hash

from app.models.user_model import Update_User_Profile
from app.services.user_service import (
    get_user_password,
    get_user_profile,
    update_user_password,
)
from app.utils.response_message import ClientErrorMessage

bp = Blueprint(name='user_profile', import_name=__name__, url_prefix='/v1')


@bp.get('/profile')
@jwt_required()
def get_profile():
    app.logger.debug(current_user)

    current_user_profile = get_user_profile(current_user)

    if current_user_profile is not None:
        app.logger.debug(current_user_profile)

        # json.loads(current_user_profile)
        app.logger.debug(current_user_profile.dict())

        # json.dumps(current_user_profile)
        app.logger.debug(current_user_profile.json())

        return jsonify(current_user_profile.dict()), 200
    else:
        abort(404)


def check_password(hashed_password: str, password: str):
    return check_password_hash(hashed_password, password)


@bp.post('/profile')
@jwt_required()
def post_user_profile():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                new_user = Update_User_Profile(**body)

                app.logger.debug(new_user)

                original_password = get_user_password(
                    new_user.id).current_password  # type: ignore
                app.logger.debug(original_password)
                current_password = new_user.current_password
                app.logger.debug(current_password)

                if original_password is not None:
                    if check_password(original_password,
                                      current_password):  # type: ignore
                        update_user_password(new_user)
                        return Response(status=204)

                    return abort(400,
                                 ClientErrorMessage.wrong_email_or_password)
                else:
                    abort(404)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)
