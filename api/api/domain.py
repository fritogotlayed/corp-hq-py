"""
The MIT License (MIT)
Copyright (c) 2017 fritogotlayed

For full license details please see the LICENSE file located in the root folder
of the project.
"""
import random
from datetime import datetime, timedelta
import string

import bcrypt

from api import repos
from api.errors import ValidationError


class Session(object):
    """Class to house the domain logic for sessions"""

    def __init__(self, session_repo: repos.SessionRepo = None):
        self._session_repo = session_repo or repos.SessionRepo()

    @staticmethod
    def _generate_token(size=128, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def create(self, payload):
        """Create a new session for the given payload"""
        required_keys = ['addressChain', 'username']

        for key in required_keys:
            if key not in payload or not payload[key]:
                raise ValidationError('Missing required key: %s' % key)

        expiry = datetime.utcnow() + timedelta(minutes=10)
        data = {
            'token': self._generate_token(),
            'addressChain': payload['addressChain'],
            'username': payload['username'],
            'userRole': 'user',
            'expireAt': expiry
        }
        self._session_repo.save(data)

        del data['addressChain']
        del data['username']

        return data

    def expire(self, payload):
        """Expire the provided payload"""
        self._session_repo.remove(payload)


class User(object):
    """Class to house the domain logic for users"""

    def __init__(self, user_repo: repos.UserRepo = None):
        self._user_repo = user_repo or repos.UserRepo()

    def authenticate(self, username, password):
        """Attempt to authenticate the user with the provided credentials"""
        db_user = self._user_repo.get_by_keys({'username': username})
        return False if db_user is None else bcrypt.checkpw(
            password, db_user.password)

    def create(self, payload):
        """Create a new user in the system"""
        required_keys = ['username', 'password', 'email']

        for key in required_keys:
            if key not in payload or not payload[key]:
                raise ValidationError('Missing required key: %s' % key)

        password = payload['password'].encode('utf8')
        data = {
            'username': payload['username'],
            'password': bcrypt.hashpw(password, bcrypt.gensalt()),
            'email': payload['email']
        }

        self._user_repo.save(data)


class DataUtilities(object):
    """Class to house the domain logic for data initialization"""

    def __init__(self,
                 region_repo: repos.RegionRepo = None,
                 region_api: repos.EveRegionRepo = None,
                 session_repo: repos.SessionRepo = None):
        self._region_repo = region_repo or repos.RegionRepo()
        self._region_api = region_api or repos.EveRegionRepo()
        self._session_repo = session_repo or repos.SessionRepo()

    def apply_indexes(self):
        """Coordinate applying indexes to the data store"""
        self._session_repo.apply_indexes()

    def populate_regions(self, force=False):
        """Coordinate loading regions from the EVE endpoints."""
        if force or not self._region_repo.has_any():
            region_ids = self._region_api.get_region_ids()
            for region_id in region_ids:
                details = self._region_api.get_region_details(region_id)
                self._region_repo.save(details)
