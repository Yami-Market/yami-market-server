from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    current_user,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)
from pydantic import ValidationError

from app.models.user_model import NewUser, UserBodyParams, UserResetPassword
from app.services.user_service import (
    check_password,
    create_new_user,
    get_user_by_email,
    get_user_by_id,
    update_user_password,
)
from app.utils.response_message import ClientErrorMessage

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/v1')


@bp.post('/signup')
def signup():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                new_user = NewUser(**body)

                app.logger.debug(new_user)

                exist_user = get_user_by_email(new_user.email)

                if exist_user is not None:
                    return abort(400, ClientErrorMessage.email_already_exists)

                create_new_user(new_user)

                return jsonify(message='Signup success')

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


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


@bp.post('/logout')
def logout():
    response = jsonify({'msg': 'logout successful'})
    unset_jwt_cookies(response)
    return response


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

                        response = jsonify(
                            {'msg': 'reset password successful'})
                        unset_jwt_cookies(response)
                        return response
                    else:
                        return abort(401, ClientErrorMessage.wrong_password)
                else:
                    abort(404)
            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)
