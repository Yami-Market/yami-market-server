from flask import Blueprint, redirect, url_for

bp = Blueprint(name='index', import_name=__name__)


@bp.route('/')
def index():
    return redirect(url_for('index.v1'))


@bp.route('/v1')
def v1():
    return 'Yami Market API v1'
