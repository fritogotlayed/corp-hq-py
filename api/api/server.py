"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from __future__ import print_function

import glob
import importlib
import logging
import os
from os import path

import flask

from api import global_hooks

CURRENT_DIR = path.abspath(__file__).replace('.pyc', '.py').replace(
    'server.py', '')
DEFAULT_LOG_FORMAT = ('%(asctime)s - %(process)s - %(thread)s - '
                      '%(levelname)s - %(module)s - %(funcName)s - '
                      '%(lineno)s - %(message)s')


def _register_blueprints(app):
    """Scans the 'controllers' folder for controller modules

    Scans the "controllers" folder for modules that have a attribute named
    "MOD". These modules are then automatically registered with the flask
    application.

    :param app: The flask application
    """
    modules = glob.glob(CURRENT_DIR + 'controllers/*.py')
    raw_mods = [path.basename(f)[:-3] for f in modules if path.isfile(f)]

    for mod in raw_mods:
        controller = importlib.import_module('api.controllers.' + mod)
        if hasattr(controller, 'MOD'):
            app.register_blueprint(controller.MOD)


def configure_logging(app: flask.Flask):
    """Setup logging for our application

    We print to std out here so that container hosts may log however they wish
    """
    logger = logging.getLogger('corp-hq')
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        os.environ.get('CORP_HQ_LOG_FORMAT', DEFAULT_LOG_FORMAT))

    logger.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    app.logger.addHandler(stream_handler)
    logger.addHandler(stream_handler)


def build_app() -> flask.Flask:
    """Builds the flask application"""
    app = flask.Flask(
        'Extended-UVA-Judge',
        template_folder='templates',
        static_folder='static')

    configure_logging(app)
    _register_blueprints(app)
    global_hooks.initialize_hooks(app)

    return app
