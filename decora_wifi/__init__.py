# Python module for controlling Leviton Decora Smart WiFi Switches
# Reverse engineered from the myLeviton Android app.
#
# Copyright 2017 Tim Lyakhovetskiy <tlyakhov@gmail.com>
#
# This code is released under the terms of the MIT license. See the LICENSE
# file for more details.

import json

import requests

from .models.person import Person


class DecoraWiFiSession:
    """This class represents an authorized HTTPS session with the LCS API."""

    LEVITON_ROOT = 'https://my.leviton.com/api'
    REQUEST_TIMEOUT_SECS = 15

    def __init__(self):
        """Initialize the session, all content is JSON."""
        self._session = requests.Session()
        self._session.headers.update({'Content-Type': 'application/json'})
        self._email = None
        self._password = None
        self.user = None

    def call_api(self, api, payload=None, method='get'):
        """Generic method for calling LCS REST APIs."""
        # Sanity check parameters first...
        if (method != 'get' and method != 'post' and
           method != 'put' and method != 'delete'):
            msg = "Tried decora.call_api with bad method: {0}"
            raise BadMethodError(msg.format(method))

        if self.user is None and api != '/Person/login':
            raise NoLoginError('Tried an API call without a login.')

        uri = self.LEVITON_ROOT + api

        # Payload is always JSON
        if payload is not None:
            payload_json = json.dumps(payload)
        else:
            payload_json = ''

        response = getattr(self._session, method)(
            uri,
            data=payload_json,
            timeout=self.REQUEST_TIMEOUT_SECS)

        # Unauthorized
        if response.status_code == 401 or response.status_code == 403:
            # Maybe we got logged out? Let's try logging in.
            if api == '/Person/login' or self.login(self._email, self._password) is None:
                raise AuthExpiredError("Auth expired and unable to refresh")
            # Retry the request...
            response = getattr(self._session, method)(
                uri,
                data=payload_json,
                timeout=self.REQUEST_TIMEOUT_SECS)

        if response.status_code != 200 and response.status_code != 204:
            msg = "myLeviton API call ({0}) failed: {1}, {2}".format(
                          api, response.status_code, response.text)
            raise ApiCallFailedError(msg)

        if response.text is not None and len(response.text) > 0:
            return json.loads(response.text)
        else:
            return None

    def login(self, email, password):
        """Login to LCS & save the token for future commands."""
        payload = {
            'email': email,
            'password': password,
            'clientId': 'levdb-echo-proto',  # from myLeviton App
            'registeredVia': 'myLeviton'     # from myLeviton App
        }

        login_json = Person.login(self, payload)

        if login_json is None:
            self._email = None
            self._password = None
            self._user = None
            return None

        self._session.headers.update({'authorization': login_json['id']})
        self._email = email
        self._password = password
        self.user = Person(self, login_json['userId'])
        self.user.refresh()

        return self.user

class DecoraWiFiError(ValueError):
    """Base class for named errors in decora_wifi."""
    pass

class BadMethodError(DecoraWiFiError):
    """Tried a decora_wifi api call with an unsupported method."""
    pass

class NoLoginError(DecoraWiFiError):
    """Tried a decora_wifi api call without a logged-in session."""
    pass

class AuthExpiredError(DecoraWiFiError):
    """API Session authentication expired and unable to refresh."""
    pass

class ApiCallFailedError(DecoraWiFiError):
    """API Call failed (returned a code other than 200 or 204)."""
    pass
