"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""

# Eve
# NOTE(Frito): Should we just store this in the DB?
ENV_EVE_API_HOST = (
    'https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')
ENV_EVE_API_USER_AGENT = (
    'Corp-HQ client https://github.com/fritogotlayed/corp-hq-api and '
    'https://github.com/fritogotlayed/corp-hq-ui contact <FritoGotLayed> '
    'in game or <Frito> on Tweetfleet')

###
# Environment
###
ENV_FLASK_HOST = 'CORP_HQ_FLASK_HOST'
ENV_FLASK_PORT = 'CORP_HQ_FLASK_PORT'
ENV_MONGO_HOST = 'CORP_HQ_MONGO_HOST'

###
# System
#
# This space is for constants generally used by the system overall.
###
SYS_LOGGER_NAME = 'corp-hq'
