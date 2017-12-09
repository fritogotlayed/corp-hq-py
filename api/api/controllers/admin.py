"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from flask import Blueprint, Response

from api.controllers import _build_response
from api.helpers import time_it
from api import domain

MOD = Blueprint('admin', __name__, url_prefix='/admin')


@MOD.route('/configured', methods=['GET'])
@time_it
def is_configured() -> Response:
    """Has the system been configured"""
    return _build_response({'is_configured': False})


@MOD.route('/configure', methods=['POST'])
@time_it
def configure() -> Response:
    """Run the code that configures the system for operation."""
    utilities = domain.DataUtilities()
    utilities.apply_indexes()
    utilities.populate_regions()
    return _build_response({'is_configured': True})
