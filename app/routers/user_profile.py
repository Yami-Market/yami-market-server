from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify
from flask_jwt_extended import current_user, jwt_required

# from app.models.user_model import User
from app.services.user_service import get_user_profile

# from app.utils.response_message import ClientErrorMessage

# from pydantic import ValidationError

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


# def get_user_profile():
#     if request.is_json:
#         body = request.get_json()
#         if body is not None:
#             try:
#                 new_user = NewUser(**body)

#                 app.logger.debug(new_user)

#                 exist_user = get_user_by_email(new_user.email)

#                 if exist_user is not None:
#                     return abort(400, ClientErrorMessage.email_already_exists)

#                 create_new_user(new_user)

#                 return jsonify(message='Signup success')

#             except ValidationError as e:
#                 return jsonify(e.errors()), 400
#         else:
#             abort(400)
#     else:
#         abort(415)
