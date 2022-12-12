import json
from typing import cast

from flask import Blueprint, abort
from flask import current_app as app
from flask import jsonify, request
from flask.wrappers import Response
from flask_jwt_extended import current_user, jwt_required
from pydantic import ValidationError

from app.models.address_model import AddressBodyParams
from app.models.credit_card_model import CreditCardBodyParams
from app.services.address_service import create_new_address, get_address_list
from app.services.credit_card_service import (
    create_credit_card,
    delete_credit_card,
    get_credit_card_list,
)

bp = Blueprint(name='credit_card', import_name=__name__, url_prefix='/v1')


@bp.get('/creditcard')
@jwt_required()
def get_credit_card():

    user_credit_card_list = get_credit_card_list(current_user)
    user_address_list = get_address_list(current_user, 'billing')

    credit_card_with_billing_address_list = []

    for credit_card in user_credit_card_list.items:
        for address in user_address_list.items:
            if credit_card.billing_address_id == address.id:
                credit_card_with_billing_address_list.append({
                    **json.loads((credit_card.json())), 'billing_address': {
                        **json.loads((address.json()))
                    }
                })
                break

    return jsonify(items=credit_card_with_billing_address_list), 200


@bp.post('/creditcard')
@jwt_required()
def create_user_credit_card():
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                credit_card_params = CreditCardBodyParams(**body)
                app.logger.debug(credit_card_params)

                billing_address = credit_card_params.billing_address

                new_address = create_new_address(
                    current_user, cast(AddressBodyParams, billing_address),
                    'billing')

                app.logger.debug(new_address)

                if new_address is not None:
                    create_credit_card(current_user, new_address.id,
                                       credit_card_params.credit_card)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.put('/creditcard/<string:credit_card_id>')
@jwt_required()
def update_user_credit_card(credit_card_id: str):
    if request.is_json:
        body = request.get_json()
        if body is not None:
            try:
                credit_card_params = CreditCardBodyParams(**body)
                app.logger.debug(credit_card_params)

                billing_address = credit_card_params.billing_address

                new_address = create_new_address(
                    current_user, cast(AddressBodyParams, billing_address),
                    'billing')

                if new_address is not None:
                    create_credit_card(current_user, new_address.id,
                                       credit_card_params.credit_card)

                delete_credit_card(current_user, credit_card_id)

                return Response(status=204)

            except ValidationError as e:
                return jsonify(e.errors()), 400
        else:
            abort(400)
    else:
        abort(415)


@bp.delete('/creditcard/<string:credit_card_id>')
@jwt_required()
def delete_user_credit_card(credit_card_id: str):
    delete_credit_card(current_user, credit_card_id)

    return Response(status=204)
