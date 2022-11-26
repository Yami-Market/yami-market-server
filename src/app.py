import os

from flask import Flask, redirect, url_for

from routers.v1.shopping_cart import shopping_cart

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'secret'

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY


@app.route('/')
def index():
    return redirect(url_for('index_v1'))


@app.route('/v1')
def index_v1():
    return 'Yami Market API v1'


# Register the shopping cart blueprint
app.register_blueprint(shopping_cart)


# Bad Request handler
@app.errorhandler(400)
def bad_request(error):
    return {'message': error.description}, 400


# Not Found handler
@app.errorhandler(404)
def not_found(error):
    return {'message': error.description}, 404


# Method Not Allowed handler
@app.errorhandler(405)
def method_not_allowed(error):
    return {'message': 'method not allowed'}, 405


# Server Error handler
@app.errorhandler(500)
def server_error(error):
    return {'message': 'server error'}, 500


# Server Uncatched Error handler
@app.errorhandler(Exception)
def uncatched_error(error):
    return {'message': 'server error'}, 500


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
