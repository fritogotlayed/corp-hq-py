"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import traceback
from flask import Flask, Response, current_app


def _set_headers(headers):
    if 'Access-Control-Allow-Origin' not in headers:
        headers['Access-Control-Allow-Origin'] = '*'

    if 'Access-Control-Allow-Methods' not in headers:
        headers['Access-Control-Allow-Methods'] = (
            'POST, GET, OPTIONS, PUT, DELETE')

    if 'Access-Control-Allow-Headers' not in headers:
        headers['Access-Control-Allow-Headers'] = (
            'Accept, Content-Type, Content-Length, Accept-Encoding, '
            'X-CSRF-Token, Authorization')


def initialize_hooks(app: Flask) -> None:
    """Initializes the global flask hooks for the application

    This is meant to initialize things like global error handling or other
    'global' things that should take place on every request this application
    serves."""

    @app.after_request
    def _after_each_request(response):  # pylint: disable=unused-variable
        _set_headers(response.headers)
        return response

    @app.errorhandler(Exception)
    def _on_error(_):  # pylint: disable=unused-variable
        current_app.logger.error(traceback.format_exc())
        headers = {}
        _set_headers(headers)
        return Response(None, 500, headers)
