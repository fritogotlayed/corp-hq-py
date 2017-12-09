"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from tests.controllers import BaseControllerTest


class TestHealth(BaseControllerTest):
    """Tests for the health check module"""

    def test_health_returns_200(self):
        """Test the health endpoint returns 200"""
        response = self.app.get('/health')
        self.assertEqual(200, response.status_code)
