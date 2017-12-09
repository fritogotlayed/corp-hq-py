"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import argparse
import logging
import os
from datetime import datetime

import api.constants as const
from api.repos import ConfigRepo
from api.server import build_app


def build_args_parse():
    """Build the arg_parse object

    Builds the arg_parse object to assist with parsing command line provided
    arguments.

    :return: arg parse object
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description='Extended UVa Judge')
    parser.add_argument(
        '--host',
        action='store',
        default=None,
        type=str,
        help='the host address to listen upon.')
    parser.add_argument(
        '--port',
        action='store',
        default=None,
        type=int,
        help='the host port to listen upon.')
    return parser


def build_and_start_server():
    """starts the flask application in development mode.

    This is never meant to be used in a production environment.
    """
    arg_parser = build_args_parse().parse_args()

    host = arg_parser.host or os.environ.get(const.ENV_FLASK_HOST, '0.0.0.0')
    port = arg_parser.port or int(os.environ.get(const.ENV_FLASK_PORT, '8888'))

    start = datetime.now()
    app = build_app()
    end = datetime.now()
    time = end - start

    logger = logging.getLogger(const.SYS_LOGGER_NAME)
    logger.info('Application built in %s.', time)
    logger.warning('Application is running in debug mode!')

    app.run(host=host, port=port, debug=True)


def seed_dev_data():
    repo = ConfigRepo()
    repo.save({
        'key': 'eve_api_url',
        'value': 'https://esi.tech.ccp.is/latest/swagger.json?'
                 'datasource=tranquility'
    })  # yapf: disable
    repo.save({
        'key': 'eve_api_user_agent',
        'value': 'Corp-HQ client https://github.com/fritogotlayed/corp-hq-api '
                 'and https://github.com/fritogotlayed/corp-hq-ui contact '
                 '<FritoGotLayed> in game or <Frito> on Tweetfleet'
    })  # yapf: disable


if __name__ == '__main__':
    seed_dev_data()
    build_and_start_server()
