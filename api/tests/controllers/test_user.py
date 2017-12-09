"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import json
from contextlib import ExitStack
from datetime import datetime
from unittest.mock import patch, MagicMock, ANY

from api.errors import ValidationError
from tests.controllers import BaseControllerTest


# pylint: disable=invalid-name
class TestUser(BaseControllerTest):
    """Tests for the health check module"""

    def test_login_valid_credentials(self):
        """Test the login when valid credentials are provided."""
        with ExitStack() as stack:
            # Arrange
            mock_session = MagicMock()
            mock_domain = stack.enter_context(
                patch('api.controllers.user.domain'))
            stack.enter_context(patch('api.helpers.logging'))
            mock_domain.Session.return_value = mock_session
            mock_session.create.return_value = {
                'expireAt': datetime.now(),
                'token': 'test token'
            }

            post_body = {'un': 'test', 'pw': 'pass'}

            # Act
            response = self.app.post(
                '/login',
                data=json.dumps(post_body),
                content_type='application/json')
            response_data = json.loads(response.data.decode('utf-8'))

            # Assert
            self.assertEqual(response.status_code, 200)
            response_keys = response_data.keys()
            self.assertIn('token', response_keys)
            self.assertIn('expires', response_keys)
            self.assertEqual(response_data['token'], 'test token')

    def test_register_valid_information(self):
        """Test the login when valid credentials are provided."""
        with ExitStack() as stack:
            # Arrange
            mock_user = MagicMock()
            stack.enter_context(patch('api.helpers.logging'))
            mock_domain = stack.enter_context(
                patch('api.controllers.user.domain'))
            mock_domain.User.return_value = mock_user

            # Act
            response = self.app.post(
                '/register',
                data=json.dumps({}),
                content_type='application/json')

            # Assert
            mock_user.create.assert_called_once_with(ANY)
            self.assertEqual(response.status_code, 201)

    def test_register_invalid_information(self):
        """Test the login when invalid credentials are provided."""
        with ExitStack() as stack:
            # Arrange
            mock_user = MagicMock()
            stack.enter_context(patch('api.helpers.logging'))
            mock_domain = stack.enter_context(
                patch('api.controllers.user.domain'))
            mock_domain.User.return_value = mock_user
            mock_user.create.side_effect = ValidationError('test error')

            # Act
            response = self.app.post(
                '/register',
                data=json.dumps({}),
                content_type='application/json')
            response_data = json.loads(response.data.decode('utf-8'))

            # Assert
            mock_user.create.assert_called_once_with(ANY)
            self.assertEqual(response.status_code, 400)
            self.assertIn('message', response_data)

    def test_logout_valid_payload(self):
        """Tests the logout when a valid payload is provided."""
        with ExitStack() as stack:
            # Arrange
            mock_session = MagicMock()
            stack.enter_context(patch('api.helpers.logging'))
            mock_domain = stack.enter_context(
                patch('api.controllers.user.domain'))
            mock_domain.Session.return_value = mock_session

            # Act
            response = self.app.post(
                '/logout',
                data=json.dumps({}),
                content_type='application/json')

            # Assert
            mock_session.expire.assert_called_once_with(ANY)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(b'', response.data)
