from flask import Blueprint
from flask import current_app as app
from flask import jsonify

from app.utils.response_message import ClientErrorMessage, ServerErrorMessage

bp = Blueprint(name='errors', import_name=__name__)


# Bad Request handler
@bp.app_errorhandler(400)
def bad_request(error):
    return jsonify(message=error.description), 400


# Unauthorized handler
@bp.app_errorhandler(401)
def unauthorized(error):
    return jsonify(message=error.description), 401


# Not Found handler
@bp.app_errorhandler(404)
def not_found(error):
    return jsonify(message=error.description), 404


# Method Not Allowed handler
@bp.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify(message=ClientErrorMessage.method_not_allowed), 405


# Server Error handler
@bp.app_errorhandler(500)
def server_error(error):
    app.logger.error(error)
    return jsonify(message=ServerErrorMessage.server_error), 500
