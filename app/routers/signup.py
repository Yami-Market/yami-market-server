from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from pydantic import ValidationError

from app.models.user_model import NewUser
from app.services.user_service import create_new_user, get_user_by_email
from app.utils.response_message import ClientErrorMessage

bp = Blueprint(name='signup', import_name=__name__, url_prefix='/v1')


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
            abort(400, ClientErrorMessage.empty_json_body)
    else:
        abort(400, ClientErrorMessage.invalid_json_body)
