"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from contextlib import ExitStack
import unittest
from unittest.mock import patch, MagicMock, ANY, call

from api import domain
from api.errors import ValidationError


# pylint: disable=invalid-name,protected-access
class TestSession(unittest.TestCase):
    """Tests for the session domain object"""

    def test_init_without_params(self):
        """Test that arg parser looks for config element"""
        # Arrange / Act
        with patch('api.domain.repos'):
            session = domain.Session()

        # Assert
        self.assertIsNotNone(session._session_repo)

    def test_init_with_params(self):
        """Test that arg parser looks for config element"""
        # Arrange
        session_repo = MagicMock()

        # Act
        session = domain.Session(session_repo)

        # Assert
        self.assertIsNotNone(session._session_repo)
        self.assertEqual(session._session_repo, session_repo)

    def test_create_valid_payload(self):
        """Tests that a session is created when payload is correct"""
        # Arrange
        session_repo = MagicMock()
        session = domain.Session(session_repo)
        payload = {'addressChain': '127.0.0.1', 'username': 'test_user'}

        # Act
        result = session.create(payload)

        # Assert
        self.assertIn('token', result)
        self.assertIn('expireAt', result)
        session_repo.save.assert_called_once_with(ANY)

    def test_create_invalid_payload(self):
        """Tests that validation fails when missing required info."""
        # Arrange
        session_repo = MagicMock()
        session = domain.Session(session_repo)
        payload = {
            'addressChain': '127.0.0.1',
        }

        # Act
        try:
            session.create(payload)
        except ValidationError as ex:
            # Assert
            self.assertIn('Missing required key: username', ex.args[0])

    @staticmethod
    def test_expire_valid_payload():
        """Tests that session is removed when a valid payload is provided"""
        # Arrange
        session_repo = MagicMock()
        session = domain.Session(session_repo)
        payload = {'token': 'test token'}

        # Act
        session.expire(payload)

        # Assert
        session_repo.remove.assert_called_once_with(payload)


class TestUser(unittest.TestCase):
    """Tests for the user domain object"""

    def test_init_without_params(self):
        """Test that the init constructs a user_repo if none provided"""
        # Arrange / Act
        with patch('api.domain.repos'):
            user = domain.User()

        # Assert
        self.assertIsNotNone(user._user_repo)

    def test_init_with_params(self):
        """Test that the init uses provided user_repo"""
        # Arrange
        user_repo = MagicMock()

        # Act
        user = domain.User(user_repo)

        # Assert
        self.assertIsNotNone(user._user_repo)
        self.assertEqual(user._user_repo, user_repo)

    def test_check_valid_password(self):
        """Tests that when provided a valid user and valid password

        True should be returned.
        """
        with ExitStack() as stack:
            # Arrange
            user_repo = MagicMock()
            user = domain.User(user_repo)
            mock_bcrypt = stack.enter_context(patch('api.domain.bcrypt'))
            mock_bcrypt.checkpw.return_value = True

            # Act
            result = user.authenticate('test', 'test')

            # Assert
            self.assertTrue(result)

    def test_check_invalid_password(self):
        """Tests that when provided a valid user and invalid password

        False should be returned.
        """
        with ExitStack() as stack:
            # Arrange
            user_repo = MagicMock()
            user = domain.User(user_repo)
            mock_bcrypt = stack.enter_context(patch('api.domain.bcrypt'))
            mock_bcrypt.checkpw.return_value = False

            # Act
            result = user.authenticate('test', 'test')

            # Assert
            self.assertFalse(result)

    def test_check_invalid_user(self):
        """Tests that when provided a valid user and invalid password

        False should be returned.
        """
        # Arrange
        user_repo = MagicMock()
        user = domain.User(user_repo)
        user_repo.get_by_keys.return_value = None

        # Act
        result = user.authenticate('test', 'test')

        # Assert
        self.assertFalse(result)

    @staticmethod
    def test_create_user_valid_payload():
        """Tests user is saved when payload is valid

        Also test that the users password is not stored in plain text
        """
        with ExitStack() as stack:
            # Arrange
            user_repo = MagicMock()
            user = domain.User(user_repo)
            payload = {
                'username': 'test.user',
                'password': 'test.password',
                'email': 'test.email@noop.us'
            }
            mock_bcrypt = stack.enter_context(patch('api.domain.bcrypt'))
            mock_bcrypt.hashpw.return_value = 'hashedpass'

            # Act
            user.create(payload)

            # Assert
            user_repo.save.assert_called_once_with(ANY)
            mock_bcrypt.hashpw.assert_called_once_with(b'test.password', ANY)

    def test_create_user_payload_missing_username(self):
        """Tests error raised when payload is missing username"""
        # Arrange
        user_repo = MagicMock()
        user = domain.User(user_repo)
        payload = {'password': '', 'email': ''}

        try:
            # Act
            user.create(payload)
        except ValidationError as ex:
            # Assert
            self.assertIn('Missing required key: username', ex.args[0])
        finally:
            user_repo.save.assert_not_called()

    def test_create_user_payload_missing_password(self):
        """Tests error raised when payload is missing username"""
        # Arrange
        user_repo = MagicMock()
        user = domain.User(user_repo)
        payload = {'username': 'test.user', 'email': ''}

        try:
            # Act
            user.create(payload)
        except ValidationError as ex:
            # Assert
            self.assertIn('Missing required key: password', ex.args[0])
        finally:
            user_repo.save.assert_not_called()


class TestDataUtility(unittest.TestCase):
    """Tests for the user domain object"""

    def test_init_without_params(self):
        """Test that the init constructs dependencies if none provided"""
        # Arrange / Act
        with ExitStack() as stack:
            stack.enter_context(patch('api.domain.repos'))
            utility = domain.DataUtilities()

        # Assert
        self.assertIsNotNone(utility._region_repo)
        self.assertIsNotNone(utility._region_api)
        self.assertIsNotNone(utility._session_repo)

    def test_init_with_params(self):
        """Test that the init uses provided dependencies"""
        # Arrange
        region_repo = MagicMock()
        region_api = MagicMock()
        session_repo = MagicMock()

        # Act
        utility = domain.DataUtilities(region_repo, region_api, session_repo)

        # Assert
        self.assertIsNotNone(utility._region_repo)
        self.assertEqual(utility._region_repo, region_repo)
        self.assertIsNotNone(utility._region_api)
        self.assertEqual(utility._region_api, region_api)
        self.assertIsNotNone(utility._session_repo)
        self.assertEqual(utility._session_repo, session_repo)

    @staticmethod
    def test_apply_indexes_calls_repos():
        """Test that apply indexes calls all the relevant repos"""
        # Arrange
        region_repo = MagicMock()
        region_api = MagicMock()
        session_repo = MagicMock()
        utility = domain.DataUtilities(region_repo, region_api, session_repo)

        # Act
        utility.apply_indexes()

        # Assert
        utility._session_repo.apply_indexes.assert_called_once_with()

    @staticmethod
    def test_populate_regions_saves_fetched_region_details():
        """Tests that populate regions gets details for discovered regions"""
        # Arrange
        region_repo = MagicMock()
        region_api = MagicMock()
        session_repo = MagicMock()
        utility = domain.DataUtilities(region_repo, region_api, session_repo)

        region_repo.has_any.return_value = False

        details_1 = {}
        details_2 = {}
        details_3 = {}

        region_api.get_region_ids.return_value = [1, 2, 3]
        region_api.get_region_details.side_effect = [
            details_1, details_2, details_3
        ]

        # Act
        utility.populate_regions()

        # Assert
        calls = [call(details_1), call(details_2), call(details_3)]
        region_repo.save.assert_has_calls(calls)
