"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""

# NOTE: This is a entry point for the docker container
# https://github.com/tiangolo/uwsgi-nginx-flask-docker
# If you are trying to run this locally as a developer
# please see developer.py

from api.server import build_app

app = build_app()
