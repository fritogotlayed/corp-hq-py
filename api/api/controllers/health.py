"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from flask import Blueprint, Response

MOD = Blueprint('health', __name__, url_prefix='')


@MOD.route('/health')
def health() -> Response:
    """Health check endpoint"""
    return Response('OK', 200)
