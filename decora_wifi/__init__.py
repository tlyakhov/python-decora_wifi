# Python module for controlling Leviton Decora Smart WiFi Switches
# Reverse engineered from the myLeviton Android app.
#
# Copyright 2017 Tim Lyakhovetskiy <tlyakhov@gmail.com>
#
# This code is released under the terms of the MIT license. See the LICENSE
# file for more details.

import requests
import json


class decora_wifi:
    """This class represents an authorized HTTPS session with the LCS API."""

    LEVITON_ROOT = 'https://my.leviton.com/api'

    def __init__(self):
        """Initialize the session, all content is JSON."""
        self._session = requests.Session()
        self._session.headers.update({'Content-Type': 'application/json'})
        self._user_id = None
        self._email = None
        self._password = None

    def call_api(self, api, payload=None, method='get'):
        """Generic method for calling LCS REST APIs."""
        # Sanity check parameters first...
        if method != 'get' and method != 'post' and method != 'put':
            msg = "Tried decora.call_api with bad method: {0}"
            raise ValueError(msg.format(method))

        if self._user_id is None and api != '/Person/login':
            raise ValueError('Tried an API call without a login.')

        uri = self.LEVITON_ROOT + api

        if payload is not None:
            payload_json = json.dumps(payload)
        else:
            payload_json = ''

        response = getattr(self._session, method)(uri, data=payload_json)

        # Unauthorized
        if response.status_code == 401 or response.status_code == 403:
            # Maybe we got logged out? Let's try logging in.
            self.login(self._email, self._password)
            # Retry the request...
            response = getattr(self._session, method)(uri, data=payload_json)

        if response.status_code != 200 and response.status_code != 204:
            msg = "myLeviton API call ({0}) failed: {1}, {2}".format(
                          api, response.status_code, response.body)
            raise ValueError(msg)

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

        login_json = self.call_api('/Person/login', payload, 'post')

        if login_json is None:
            return None

        self._session.headers.update({'authorization': login_json['id']})
        self._user_id = login_json['userId']
        self._email = email
        self._password = password

        return login_json

    def logout(self):
        """Logout of LCS."""
        if self._user_id is None:
            return None

        return self.call_api('/Person/logout', None, 'post')

    def residential_permissions(self):
        """Get Leviton residential permissions objects."""
        api = "/Person/{0}/residentialPermissions".format(self._user_id)
        return self.call_api(api, None, 'get')

    def residences(self, res_account_id):
        """Get Leviton residence objects."""
        api = "/ResidentialAccounts/{0}/Residences".format(res_account_id)
        return self.call_api(api, None, 'get')

    def iot_switches(self, residence_id):
        """Get Leviton switch objects."""
        api = "/Residences/{0}/iotSwitches".format(residence_id)
        return self.call_api(api, None, 'get')

    def iot_switch_data(self, switch_id):
        """Get Leviton switch attributes for a particular id."""
        api = "/IotSwitches/{0}".format(switch_id)
        return self.call_api(api, None, 'get')

    def iot_switch_update(self, switch_id, attribs):
        """Update a Leviton switch with new attributes."""
        api = "/IotSwitches/{0}".format(switch_id)
        return self.call_api(api, attribs, 'put')
