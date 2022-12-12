from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.user_model import UpdateUserProfile, UserResetPassword
from app.services.user_service import (
    check_password,
    get_user_by_id,
    get_user_profile,
    update_user_password,
    update_user_profile,
)
from app.utils.response_message import ClientErrorMessage

bp = Blueprint(name='user_profile', import_name=__name__, url_prefix='/v1')


@bp.get('/profile')
@jwt_required()
def get_profile():
    # app.logger.debug(current_user)

    current_user_profile = get_user_profile(current_user)

    if current_user_profile is not None:
        app.logger.debug(current_user_profile)

        # json.loads(current_user_profile)
        # app.logger.debug(current_user_profile.dict())

        # json.dumps(current_user_profile)
        # app.logger.debug(current_user_profile.json())

        return jsonify(current_user_profile.dict()), 200
    else:
        abort(404)


@bp.post('/profile')
@jwt_required()
def post_profile():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                new_profile = UpdateUserProfile(**body)
                app.logger.debug(new_profile)
                user = get_user_by_id(current_user.id)
                app.logger.debug(current_user)
                if user is not None:
                    update_user_profile(new_profile, user.id)
                    return Response(status=204)
                else:
                    abort(404)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.post('/resetpassword')
@jwt_required()
def reset_password():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                reset_password = UserResetPassword(**body)

                user = get_user_by_id(current_user.id)
                app.logger.debug(user)

                if user is not None:
                    if check_password(user.password,
                                      reset_password.current_password):
                        update_user_password(current_user,
                                             reset_password.new_password)

                        return Response(status=204)
                    else:
                        return abort(400, ClientErrorMessage.wrong_password)
                else:
                    abort(404)
            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)

    #                                   current_password):
    # current_password = new_user.current_password
    # app.logger.debug(current_password)

    #             if original_password is not None:
    #                 if check_password(original_password,
    #                                   current_password):  # type: ignore
    #                     update_user_password(new_user)
    #                     return Response(status=204)
    #  return abort(400,
    #                              ClientErrorMessage.wrong_email_or_password)
