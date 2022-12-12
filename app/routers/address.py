import json

from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.address_model import AddressBodyParams
from app.services.address_service import (
    create_new_address,
    delete_address,
    get_address_list,
)

bp = Blueprint(name='address', import_name=__name__, url_prefix='/v1')


@bp.get('/shippingaddress')
@jwt_required()
def get_shipping_address():
    user_address_list = get_address_list(current_user)

    return jsonify(json.loads(user_address_list.json())), 200


@bp.post('/address')
@jwt_required()
def create_address():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                address_params = AddressBodyParams(**body)

                app.logger.debug(address_params)

                create_new_address(current_user, address_params)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.put('/address/<string:address_id>')
@jwt_required()
def update_user_address(address_id):
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                address_params = AddressBodyParams(**body)

                app.logger.debug(address_params)

                create_new_address(current_user, address_params)

                delete_address(current_user, address_id)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.delete('/address/<string:address_id>')
@jwt_required()
def delete_user_address(address_id):
    delete_address(current_user, address_id)

    return Response(status=204)
