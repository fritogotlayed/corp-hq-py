"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import unittest

from api import server


class BaseControllerTest(unittest.TestCase):
    """Tests for the health check module"""

    def setUp(self):
        """Common setup code for all controller module endpoints"""
        app = server.build_app()
        app.testing = True
        self.app = app.test_client()  # type: FlaskClient

    def tearDown(self):
        """Common tear down code for all controller module endpoints"""
        pass
