from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from pydantic import ValidationError

from app.models.user import NewUser
from app.services.user import create_new_user, get_user_by_email

bp = Blueprint(name='signup', import_name=__name__, url_prefix='/v1')


@bp.route('/signup', methods=['POST'])
def signup():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                new_user = NewUser(**body)
                new_user2 = NewUser(**body)

                app.logger.debug(new_user)
                app.logger.debug(new_user2)

                app.logger.debug(new_user)

                exist_user = get_user_by_email(new_user.email)

                if exist_user is not None:
                    return abort(400, 'email already exists')

                create_new_user(new_user)

                return jsonify(message='signup success')

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400, 'request body is empty')
    else:
        abort(400, 'request body is not json')
