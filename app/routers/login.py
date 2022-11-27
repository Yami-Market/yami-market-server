from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import create_access_token
from pydantic import ValidationError

from app.models.user import User

bp = Blueprint(name='login', import_name=__name__, url_prefix='/v1')


@bp.route('/login', methods=['POST'])
def login():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                user = User(**body)
                print(user)

                if user.email != 'admin@email.com' or user.password != 'admin':
                    abort(401, 'Invalid email or password')

                access_token = create_access_token(identity=user.email)
                return jsonify(access_token=access_token)

            except ValidationError:
                abort(400, 'JSON data is not correct')

        else:
            abort(400, 'request body is empty')
    else:
        abort(400, 'request body is not json')
