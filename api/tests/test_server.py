"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import unittest

import api.server as server


class TestServer(unittest.TestCase):
    """Tests for the server module"""

    def test_build_app(self):
        """Test that we can successfully build the flask application"""
        # Act
        app = server.build_app()

        # Assert
        self.assertIsNotNone(app)
