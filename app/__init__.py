import logging
from datetime import datetime, timedelta, timezone

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
)
from rich.logging import RichHandler

from app.extensions.jwt import jwt
from app.utils.logger import remove_color_filter
from config import DevelopmentConfig


def create_app(config_class: object = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app,
         resources={r'/*': {
             'origins': 'http://localhost:3000'
         }},
         supports_credentials=True)

    jwt.init_app(app)

    # Pretty print logs
    if app.config['DEBUG']:
        logging.basicConfig(level='NOTSET',
                            format='%(message)s',
                            datefmt='[%X]',
                            handlers=[RichHandler(rich_tracebacks=True)])
        logging.getLogger('werkzeug').addFilter(remove_color_filter)

    # Using an `after_request` callback, we refresh any token that is within 30
    # minutes of expiring.
    # Change the timedeltas to match the needs of your application.
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()['exp']
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT.
            # Just return the original response
            return response

    # Register blueprint
    from app.routers.index import bp as index_bp
    app.register_blueprint(index_bp)

    from app.routers.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.routers.signup import bp as signup_bp
    app.register_blueprint(signup_bp)

    from app.routers.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.routers.shopping_cart import bp as shopping_cart_bp
    app.register_blueprint(shopping_cart_bp)

    from app.routers.user_profile import bp as user_profile_bp
    app.register_blueprint(user_profile_bp)

    from app.routers.category import bp as category_bp
    app.register_blueprint(category_bp)

    from app.routers.product import bp as product_bp
    app.register_blueprint(product_bp)

    from app.routers.special_product import bp as special_product_bp
    app.register_blueprint(special_product_bp)

    from app.routers.address import bp as address_bp
    app.register_blueprint(address_bp)

    from app.routers.credit_card import bp as credit_card_bp
    app.register_blueprint(credit_card_bp)

    app.logger.debug(app.url_map)

    return app
