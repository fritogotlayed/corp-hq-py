"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
from abc import ABCMeta, abstractmethod
import logging
import os
import random
from time import sleep

import esipy
from pymongo.collection import Collection
from pymongo import MongoClient
import api.constants as const


def retry(limit):
    """Retry wrapper for any method"""

    def _wrap(func):
        def _wrapped(*args, **kwargs):
            logger = logging.getLogger(const.SYS_LOGGER_NAME)
            tries = 0
            while tries < limit:
                try:
                    tries += 1
                    result = func(*args, **kwargs)
                    return result
                except Exception as ex:  # pylint: disable=broad-except
                    sleep(random.randint(tries, tries * 3))
                    if tries == limit:
                        logger.error(ex)
                        raise
                    else:
                        logger.warning(ex)

        return _wrapped

    return _wrap


class BaseRepo:
    """Base repo for all repositories that act against the corp-hq database"""
    __metaclass__ = ABCMeta

    def __init__(self, client: MongoClient = None):
        self._db = None
        self._client = client or MongoClient(
            host=os.environ.get(const.ENV_MONGO_HOST))

    @property
    @abstractmethod
    def _keys(self) -> list:
        """Provides the list of primary keys for this document"""
        raise NotImplementedError

    @property
    @abstractmethod
    def _col(self) -> Collection:
        raise NotImplementedError

    def _validate(self, item):
        for key in self._keys:
            if key not in item:
                raise ValueError(key)

    def _build_filter(self, item):
        key_filter = {}
        for key in self._keys:
            key_filter[key] = item[key]
        return key_filter

    def save(self, item):
        """Save the provided item to the database after verification passes"""
        self._validate(item)
        self._col.replace_one(self._build_filter(item), item, upsert=True)

    def get_by_keys(self, keys):
        """Load the item from the database that matches the provided keys"""
        self._validate(keys)
        return self._col.find_one(keys)

    def remove(self, item):
        """Delete the item from the database that matches the provided keys"""
        self._validate(item)
        self._col.delete_one(self._build_filter(item))


class BaseEveRepo:  # pylint: disable=too-few-public-methods
    """Base repo for all repositories that act against the EVE APIs"""
    __metaclass__ = ABCMeta

    _ESI_APP = None
    _ESI_CLIENT = None

    def __init__(self, config_repo=None, app=None, client=None):
        """ Initialize the components for the base Eve repository.

        :param config_repo: The config repo where connection details are stored
        :type config_repo: ConfigRepo

        :param app: The esi application from which to generate requests
        :type app: esipy.App

        :param client: The esi client with which to execute requests
        :type client: esipy.EsiClient
        """
        self._config_repo = config_repo or ConfigRepo()

        if not app and not BaseEveRepo._ESI_APP:
            BaseEveRepo._ESI_APP = esipy.App.create(
                url=self._config_repo.get_by_keys({
                    'key': 'eve_api_url'
                })['value'])

        if not client and not BaseEveRepo._ESI_CLIENT:
            BaseEveRepo._ESI_CLIENT = esipy.EsiClient(
                retry_requests=True,
                header={
                    'User-Agent':
                    self._config_repo.get_by_keys({
                        'key': 'eve_api_user_agent'
                    })['value']
                },
                raw_body_only=False)

        self._app = app or BaseEveRepo._ESI_APP
        self._client = client or BaseEveRepo._ESI_CLIENT


class RegionRepo(BaseRepo):
    """Class to house region specific data layer operations"""

    def __init__(self, client: MongoClient = None):
        super().__init__(client)

        self._db = self._client['eve-static-data']

    @property
    def _keys(self):
        return ['region_id']

    @property
    def _col(self) -> Collection:
        return self._db['regions']

    def has_any(self) -> bool:
        """True if there are any records in the database, false otherwise"""
        return self._col.count() != 0


class SessionRepo(BaseRepo):
    """Class to house session specific data layer operations"""

    def __init__(self, client: MongoClient = None):
        super().__init__(client)

        self._db = self._client['corp-hq']

    @property
    def _keys(self) -> list:
        return ['token']

    @property
    def _col(self) -> Collection:
        return self._db['sessions']

    def apply_indexes(self):
        """Apply session specific indexes to the database"""
        self._col.create_index('expireAt', expireAfterSeconds=1)


class UserRepo(BaseRepo):
    """Class to house user specific data layer operations"""

    def __init__(self, client: MongoClient = None):
        super().__init__(client)

        self._db = self._client['corp-hq']

    @property
    def _keys(self) -> list:
        return ['username']

    @property
    def _col(self) -> Collection:
        return self._db['users']


class ConfigRepo(BaseRepo):
    """Class to house system configuration specific data layer operations"""

    def __init__(self, client: MongoClient = None):
        super().__init__(client)

        self._db = self._client['corp-hq']

    @property
    def _keys(self):
        return ['key']

    @property
    def _col(self):
        return self._db['config']


class EveRegionRepo(BaseEveRepo):
    """Class to house region operations against the eve APIs."""

    def __init__(self,
                 app=None,
                 client=None,
                 config_repo=None,
                 region_repo=None):
        """
        :param app:
        :type app: esipy.App

        :param client:
        :type client: esipy.EsiClient

        :param config_repo:
        :type config_repo: ConfigRepo

        :param region_repo:
        :type region_repo: RegionRepo
        """
        super().__init__(config_repo, app, client)

        self._region_repo = region_repo or RegionRepo()

    @retry(3)
    def get_region_ids(self):
        """Gets available regions from the EVE API"""
        get_universe_regions = self._app.op['get_universe_regions']()
        response = self._client.request(get_universe_regions)
        return response.data

    @retry(3)
    def get_region_details(self, region_id):
        """Gets details of a region from the EVE API"""
        get_universe_regions_region_id = self._app.op[
            'get_universe_regions_region_id'](region_id=region_id)
        response = self._client.request(get_universe_regions_region_id)
        return response.data
