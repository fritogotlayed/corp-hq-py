"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from contextlib import ExitStack

from unittest.mock import MagicMock, patch
import unittest
from pymongo.collection import Collection
import mongomock

# pylint: disable=invalid-name,protected-access
from runner import repos
from runner import constants as const


###
# Bases
###
class EveRepoTestBase(unittest.TestCase):
    """Base test class for Eve api / client using repositories."""

    def setUp(self):
        repos.BaseEveRepo._ESI_APP = MagicMock()
        repos.BaseEveRepo._ESI_CLIENT = MagicMock()

    def tearDown(self):
        repos.BaseEveRepo._ESI_APP = None
        repos.BaseEveRepo._ESI_CLIENT = None


###
# Test Fixtures
###
class TestBaseRepo(unittest.TestCase):
    """Tests for the base repo class"""

    class NoCollectionImplementation(repos.BaseRepo):  # pylint: disable=abstract-method
        """Test implementation for missing _col property"""

        @property
        def _keys(self) -> list:
            return ['pk']

    class NoKeysImplementation(repos.BaseRepo):  # pylint: disable=abstract-method
        """Test implementation for missing _keys property"""

        @property
        def _col(self) -> Collection:
            return self._db['test-col']  # pylint: disable=unsubscriptable-object

    class Implementation(repos.BaseRepo):
        """Implementation for making BaseRepo testing easier"""

        def __init__(self, client):
            super().__init__(client)

            self._db = self._client['test-db']

        @property
        def _col(self) -> Collection:
            return self._db['test-col']

        @property
        def _keys(self) -> list:
            return ['pk']

    def test_empty_constructor_creates_client(self):
        """Tests that a client is constructed when none is provided """
        with ExitStack() as stack:
            # Arrange
            config = {const.ENV_MONGO_HOST: '10.0.0.1'}
            instance = MagicMock()
            mock_client = stack.enter_context(patch('runner.repos.MongoClient'))
            mock_client.return_value = instance
            stack.enter_context(patch('os.environ', new=config))

            # Act
            repo = repos.BaseRepo()

            # Assert
            self.assertIsNotNone(repo)
            self.assertEqual(repo._client, instance)
            mock_client.assert_called_once_with(host='10.0.0.1')

    def test_constructor_provided_client_uses_client(self):
        """Tests that a client is constructed when none is provided """
        # Arrange
        instance = MagicMock()

        # Act
        repo = repos.BaseRepo(instance)

        # Assert
        self.assertIsNotNone(repo)
        self.assertEqual(repo._client, instance)

    def test_methods_fail_on_no_collection_implementation(self):
        """Tests that actions fail when the repo has not implemented _col"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.NoCollectionImplementation(client)
        item = {'pk': 'foo', 'data': 'bar'}

        try:
            # Act
            repo.save(item)
            self.fail('Not implemented expected but not raised.')
        except NotImplementedError:
            pass

    def test_methods_fail_on_no_keys_implementation(self):
        """Tests that actions fail when the repo has not implemented _keys"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.NoKeysImplementation(client)
        item = {'pk': 'foo', 'data': 'bar'}

        try:
            # Act
            repo.save(item)
            self.fail('Not implemented expected but not raised.')
        except NotImplementedError:
            pass

    def test_save_persists_valid_item(self):
        """Tests that save persists the item to the mongo instance"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.Implementation(client)
        item = {'pk': 'foo', 'data': 'bar'}

        # Act
        repo.save(item)

        # Assert
        db_data = client['test-db']['test-col'].find_one({'pk': 'foo'})
        self.assertEqual(db_data['data'], 'bar')

    def test_save_errors_on_invalid_item(self):
        """Tests that save persists the item to the mongo instance"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.Implementation(client)
        item = {'data': 'foo', 'data2': 'bar'}

        try:
            # Act
            repo.save(item)
        except ValueError as ex:
            # Assert
            self.assertIn('pk', ex.args[0])

    def test_get_by_keys_returns_existing_document(self):
        """Tests fetch of documents based on the computed key filter"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.Implementation(client)
        item = {'pk': 'foo', 'data': 'bar'}
        client['test-db']['test-col'].save(item)

        # Act
        db_data = repo.get_by_keys({'pk': 'foo'})

        # Assert
        self.assertEqual(db_data['data'], 'bar')

    def test_get_by_keys_returns_none_for_not_found_keys(self):
        """Test we get non when searching for a key not in the collection"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.Implementation(client)
        item = {'pk': 'foo', 'data': 'bar'}
        client['test-db']['test-col'].save(item)

        # Act
        db_data = repo.get_by_keys({'pk': 'foo2'})

        # Assert
        self.assertEqual(client['test-db']['test-col'].count(), 1)
        self.assertIsNone(db_data)

    def test_remove_deletes_item(self):
        """Test we remove items from the collection properly"""
        # Arrange
        client = mongomock.MongoClient()
        repo = TestBaseRepo.Implementation(client)
        item = {'pk': 'foo', 'data': 'bar'}
        client['test-db']['test-col'].save(item)
        client['test-db']['test-col'].save({'pk': 'bar', 'data': 'a'})
        client['test-db']['test-col'].save({'pk': 'blah', 'data': 'b'})

        # Act
        before_count = client['test-db']['test-col'].count()
        repo.remove({'pk': 'foo'})
        after_count = client['test-db']['test-col'].count()

        # Assert
        self.assertEqual(before_count, 3)
        self.assertEqual(after_count, 2)


class TestBaseEveRepo(EveRepoTestBase):
    """Test the base eve repo properties and functionality"""

    def test_empty_constructor_creates_client(self):
        """Tests that a client is constructed when none is provided """
        with ExitStack() as stack:
            # Arrange
            repos.BaseEveRepo._ESI_APP = None
            repos.BaseEveRepo._ESI_CLIENT = None
            mock_app = MagicMock()
            mock_client = MagicMock()
            mock_config_repo = MagicMock()
            mock_app_create = stack.enter_context(
                patch('runner.repos.esipy.App.create'))
            mock_client_init = stack.enter_context(
                patch('runner.repos.esipy.EsiClient'))
            mock_config_repo_init = stack.enter_context(
                patch('runner.repos.ConfigRepo'))

            mock_app_create.return_value = mock_app
            mock_client_init.return_value = mock_client
            mock_config_repo_init.return_value = mock_config_repo

            # Act
            repo = repos.BaseEveRepo()

            # Assert
            self.assertIsNotNone(repo)
            self.assertEqual(repo._app, mock_app)
            self.assertEqual(repo._client, mock_client)
            self.assertEqual(repo._config_repo, mock_config_repo)

    def test_constructor_provided_client_uses_client(self):
        """Tests that a client is constructed when none is provided """
        # Arrange
        mock_app = MagicMock()
        mock_client = MagicMock()
        mock_config_repo = MagicMock()

        # Act
        repo = repos.BaseEveRepo(mock_config_repo, mock_app, mock_client)

        # Assert
        self.assertIsNotNone(repo)
        self.assertEqual(repo._app, mock_app)
        self.assertEqual(repo._client, mock_client)
        self.assertEqual(repo._config_repo, mock_config_repo)

    def test_multiple_empty_constructor_creates_single_client(self):
        """Tests that a client is constructed when none is provided """
        with ExitStack() as stack:
            # Arrange
            repos.BaseEveRepo._ESI_APP = None
            repos.BaseEveRepo._ESI_CLIENT = None
            mock_app = MagicMock()
            mock_client = MagicMock()
            mock_config_repo = MagicMock()
            mock_app_create = stack.enter_context(
                patch('runner.repos.esipy.App.create'))
            mock_client_init = stack.enter_context(
                patch('runner.repos.esipy.EsiClient'))
            mock_config_repo_init = stack.enter_context(
                patch('runner.repos.ConfigRepo'))

            mock_app_create.side_effect = [mock_app, MagicMock()]
            mock_client_init.side_effect = [mock_client, MagicMock()]
            mock_config_repo_init.return_value = mock_config_repo

            # Act
            repo = repos.BaseEveRepo()
            repo2 = repos.BaseEveRepo()

            # Assert
            self.assertIsNotNone(repo)
            self.assertIsNotNone(repo2)
            self.assertEqual(repo._app, mock_app)
            self.assertEqual(repo._client, mock_client)
            self.assertEqual(repo2._app, mock_app)
            self.assertEqual(repo2._client, mock_client)


class TestRegionRepo(unittest.TestCase):
    """Test region repo properties and functionality"""

    def test_keys_initialized_properly(self):
        """Test that the keys property has been implemented properly"""
        # Arrange
        client = MagicMock()
        repo = repos.RegionRepo(client)

        # Act
        keys = repo._keys

        # Assert
        self.assertEqual(len(keys), 1)
        self.assertIn('region_id', keys)

    def test_col_initialized_properly(self):
        """Test that the col property has been implemented properly"""
        # Arrange
        mock_collection = MagicMock
        client = {'eve-static-data': {'regions': mock_collection}}
        repo = repos.RegionRepo(client)

        # Act
        collection = repo._col

        # Assert
        self.assertEqual(collection, mock_collection)

    def test_has_any_returns_true_when_data_present(self):
        """Tests that has_any returns true when data is in the collection"""
        # Arrange
        client = mongomock.MongoClient()
        repo = repos.RegionRepo(client)
        item = {'region_id': 12345, 'data': 'bar'}
        client['eve-static-data']['regions'].save(item)

        # Act
        db_result = repo.has_any()

        # Assert
        self.assertTrue(db_result)

    def test_has_any_returns_false_when_data_is_not_present(self):
        """Tests that has_any returns false when no data in the collection"""
        # Arrange
        client = mongomock.MongoClient()
        repo = repos.RegionRepo(client)

        # Act
        db_result = repo.has_any()

        # Assert
        self.assertFalse(db_result)


class TestSessionRepo(unittest.TestCase):
    """Test session repo properties and functionality"""

    def test_keys_initialized_properly(self):
        """Test that the keys property has been implemented properly"""
        # Arrange
        client = MagicMock()
        repo = repos.SessionRepo(client)

        # Act
        keys = repo._keys

        # Assert
        self.assertEqual(len(keys), 1)
        self.assertIn('token', keys)

    def test_col_initialized_properly(self):
        """Test that the col property has been implemented properly"""
        # Arrange
        mock_collection = MagicMock()
        client = {'corp-hq': {'sessions': mock_collection}}
        repo = repos.SessionRepo(client)

        # Act
        collection = repo._col

        # Assert
        self.assertEqual(collection, mock_collection)

    @staticmethod
    def test_apply_indexes_sets_indexes_on_collection():
        """Test that indexes are saved on the backing collection"""
        # Arrange
        mock_collection = MagicMock()
        client = {'corp-hq': {'sessions': mock_collection}}
        repo = repos.SessionRepo(client)

        # Act
        repo.apply_indexes()

        # Assert
        mock_collection.create_index.assert_called_once_with(
            'expireAt', expireAfterSeconds=1)


class TestUserRepo(unittest.TestCase):
    """Test user repo properties and functionality"""

    def test_keys_initialized_properly(self):
        """Test that the keys property has been implemented properly"""
        # Arrange
        client = MagicMock()
        repo = repos.UserRepo(client)

        # Act
        keys = repo._keys

        # Assert
        self.assertEqual(len(keys), 1)
        self.assertIn('username', keys)

    def test_col_initialized_properly(self):
        """Test that the col property has been implemented properly"""
        # Arrange
        mock_collection = MagicMock()
        client = {'corp-hq': {'users': mock_collection}}
        repo = repos.UserRepo(client)

        # Act
        collection = repo._col

        # Assert
        self.assertEqual(collection, mock_collection)


class TestEveRegionRepo(TestBaseEveRepo):
    """Test eve region repo properties and functionality"""

    def test_empty_constructor_creates_repo(self):
        """Test that a valid repo is constructed with no parameters"""
        with ExitStack() as stack:
            # Arrange
            mock_app = MagicMock()
            mock_client = MagicMock()
            mock_region_repo = MagicMock()
            mock_region_repo_init = stack.enter_context(
                patch('runner.repos.RegionRepo'))
            mock_region_repo_init.return_value = mock_region_repo

            # Act
            repo = repos.EveRegionRepo(mock_app, mock_client)

            # Assert
            self.assertIsNotNone(repo._region_repo)
            self.assertEqual(repo._region_repo, mock_region_repo)


class TestConfigRepo(unittest.TestCase):
    """Test user repo properties and functionality"""

    def test_keys_initialized_properly(self):
        """Test that the keys property has been implemented properly"""
        # Arrange
        client = MagicMock()
        repo = repos.ConfigRepo(client)

        # Act
        keys = repo._keys

        # Assert
        self.assertEqual(len(keys), 1)
        self.assertIn('key', keys)

    def test_col_initialized_properly(self):
        """Test that the col property has been implemented properly"""
        # Arrange
        mock_collection = MagicMock()
        client = {'corp-hq': {'config': mock_collection}}
        repo = repos.ConfigRepo(client)

        # Act
        collection = repo._col

        # Assert
        self.assertEqual(collection, mock_collection)

    def test_constructor_uses_provided_repo(self):
        """Test that a valid repo is constructed with parameters"""
        # Arrange
        mock_app = MagicMock()
        mock_client = MagicMock()
        mock_config_repo = MagicMock()
        mock_region_repo = MagicMock()

        # Act
        repo = repos.EveRegionRepo(mock_app, mock_client, mock_config_repo,
                                   mock_region_repo)

        # Assert
        self.assertIsNotNone(repo._region_repo)
        self.assertEqual(repo._region_repo, mock_region_repo)

    def test_get_region_ids_returns_retrieved_ids(self):
        """Test we get region ids from the eve client response"""
        # Arrange
        mock_app = MagicMock()
        mock_client = MagicMock()
        mock_config_repo = MagicMock()
        mock_region_repo = MagicMock()
        mock_response = MagicMock()

        mock_client.request.return_value = mock_response
        data = [1, 2, 3]
        mock_response.data = data
        repo = repos.EveRegionRepo(mock_app, mock_client, mock_config_repo,
                                   mock_region_repo)

        # Act
        return_data = repo.get_region_ids()

        # Assert
        self.assertIsNotNone(return_data)
        self.assertEqual(data, return_data)

    def test_get_region_details_returns_retrieved_details(self):
        """Test we get region details from the eve client response"""
        # Arrange
        mock_app = MagicMock()
        mock_client = MagicMock()
        mock_config_repo = MagicMock()
        mock_region_repo = MagicMock()
        mock_response = MagicMock()

        mock_client.request.return_value = mock_response
        data = {'regionId': 1, 'name': 'test'}
        mock_response.data = data
        repo = repos.EveRegionRepo(mock_app, mock_client, mock_config_repo,
                                   mock_region_repo)

        # Act
        return_data = repo.get_region_details(1)

        # Assert
        self.assertIsNotNone(data)
        self.assertEqual(data, return_data)
