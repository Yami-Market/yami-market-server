import logging

from extensions.jwt import jwt_manager
from flask import Flask, current_app, g
from psycopg2.extensions import connection
from rich.logging import RichHandler

from app.utils.logger import remove_color_filter
from config import DevelopmentConfig


def get_db_conn() -> connection:
    current_app.logger.debug('Getting db connection')
    if 'conn' not in g:
        g.conn = current_app.config['DB_POOL'].getconn()
    return g.conn


def create_app(config_class: object = DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    jwt_manager.init_app(app)

    # Pretty print logs
    if app.config['DEBUG']:
        logging.basicConfig(level='NOTSET',
                            format='%(message)s',
                            datefmt='[%X]',
                            handlers=[RichHandler(rich_tracebacks=True)])
        logging.getLogger('werkzeug').addFilter(remove_color_filter)

    @app.teardown_appcontext
    def teardown_db_conn(error):
        app.logger.debug('Closing db connection')
        conn = g.pop('conn', None)

        if conn is not None:
            app.config['DB_POOL'].putconn(conn)

    # Register blueprint
    from app.routers.index import bp as index_bp
    app.register_blueprint(index_bp)

    from app.routers.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.routers.signup import bp as signup_bp
    app.register_blueprint(signup_bp)

    # app.register_blueprint(login.bp)
    # app.register_blueprint(shopping_cart.bp)

    app.logger.debug(app.url_map)

    return app
