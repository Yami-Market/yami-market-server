import os

from flask import Flask, redirect, url_for

from routers.shopping_cart import shopping_cart

FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or 'secret'

app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY


@app.route('/')
def index():
    return redirect(url_for('v1_index'))


@app.route('/v1')
def v1_index():
    return 'Yami Market API v1'


app.register_blueprint(shopping_cart)

if __name__ == '__main__':
    app.run(debug=True)
