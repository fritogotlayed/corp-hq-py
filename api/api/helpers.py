"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from datetime import datetime
from functools import wraps
import logging

from flask import request

import api.constants as const


def time_it(func):
    """Emits the total time that the wrapped function took to execute"""

    @wraps(func)
    def _wrapped(*args, **kwargs):
        logger = logging.getLogger(const.SYS_LOGGER_NAME)
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        logger.debug('%s took %s', request.full_path, end - start)
        return result

    return _wrapped


def get_originator_ip_chain():
    """Compute the ip address chain for the current request"""
    chain = request.remote_addr

    forward_info = request.headers.get('x-forwarded-for')
    if forward_info:
        chain += ', ' + forward_info

    return chain


def update_dict_key(dictionary, old_key, new_key):
    """Updates the specified dictionary key"""
    dictionary[new_key] = dictionary[old_key]
    del dictionary[old_key]
