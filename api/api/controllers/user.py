"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import rfc3339
from flask import Blueprint, Response, request
from flask_api import status

from api.controllers import _build_response
from api.helpers import time_it, get_originator_ip_chain, update_dict_key
from api import domain
from api.errors import ValidationError

MOD = Blueprint('user', __name__, url_prefix='')


@MOD.route('/login', methods=['POST'])
@time_it
def login() -> Response:
    """User login endpoint"""
    payload = request.get_json()
    session = domain.Session()

    update_dict_key(payload, 'un', 'username')
    update_dict_key(payload, 'pw', 'password')

    payload['addressChain'] = get_originator_ip_chain()

    data = session.create(payload)
    data['expires'] = rfc3339.format(data['expireAt'], True, False)
    del data['expireAt']
    return _build_response(data)


@MOD.route('/register', methods=['POST'])
@time_it
def register() -> Response:
    """Register new user endpoint"""
    payload = request.get_json()
    user = domain.User()

    try:
        user.create(payload)
    except ValidationError as ex:
        data = {'message': ex.args[0]}
        return _build_response(data, status.HTTP_400_BAD_REQUEST)

    return _build_response(None, status.HTTP_201_CREATED)


@MOD.route('/logout', methods=['POST'])
@time_it
def logout() -> Response:
    """User login endpoint"""
    payload = request.get_json()
    session = domain.Session()

    session.expire(payload)
    return _build_response(None)
