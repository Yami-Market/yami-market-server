import logging

from flask import Flask
from flask_cors import CORS
from rich.logging import RichHandler

from app.extensions.jwt import jwt
from app.utils.logger import remove_color_filter
from config import DevelopmentConfig


def create_app(config_class: object = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt.init_app(app)
    CORS(app)

    # Pretty print logs
    if app.config['DEBUG']:
        logging.basicConfig(level='NOTSET',
                            format='%(message)s',
                            datefmt='[%X]',
                            handlers=[RichHandler(rich_tracebacks=True)])
        logging.getLogger('werkzeug').addFilter(remove_color_filter)

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

    app.logger.debug(app.url_map)

    return app
