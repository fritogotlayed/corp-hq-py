"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import json

from flask import Response
from flask_api import status as codes


def _build_response(data, status=codes.HTTP_200_OK, headers=None):
    if isinstance(data, dict):
        data = json.dumps(data)

    if not headers:
        headers = {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = 'application/json'

    return Response(data, status=status, headers=headers)
