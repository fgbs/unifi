#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import ssl
import json
from requests import Session, Request
from requests_toolbelt import SSLAdapter

# workaround to suppress InsecureRequestWarning
# See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings()

import exceptions


class Controller(object):
    def __init__(self, host='127.0.0.1', port=8443, version='v5'):
        self.host = host
        self.port = port
        self.version = version
        self.logged_in = False

        self._username = None
        self._password = None
        self._site = None
        self._baseurl = 'https://{}:{}'.format(
            self.host,
            self.port
        )

        self._session = Session()
        self._session.mount(self._baseurl, SSLAdapter(ssl.PROTOCOL_SSLv23))
        

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = value
    
    @property
    def site(self):
        if self._site is None:
            return 'default'
        return self._site
    
    @site.setter
    def site(self, value):
        self._site = value

    def _jsondec(self, data):
        obj = data.json()
        if 'meta' in obj:
            if obj['meta']['rc'] != 'ok':
                raise exceptions.APIError(obj['meta']['msg'])
        if 'data' in obj:
            return obj['data']
        return obj

    def _request(self, endpoint, data={}, method='POST'):
        if not self.logged_in:
            self.connect()

        if endpoint == 'login':
            url = '{}/api/{}'.format(self._baseurl, endpoint)
        else:
            url = '{}/api/s/{}/{}'.format(
                self._baseurl,
                self.site,
                endpoint
            )
        
        return self._jsondec(
            self._session.send(
                self._session.prepare_request(
                    Request(
                        method,
                        url,
                        data=json.dumps(data).encode('utf8'),
                        headers={
                            'Content-type': 'application/json'
                        }
                    )                    
                ),
                verify=False
            )
        )
        
    def connect(self):
        if self.username is None or self.password is None:
            raise exceptions.CredentialsMissing
        
        try:
            self.logged_in = True
            return self._request(
                'login',
                {
                    'username': self.username, 
                    'password': self.password
                }
            )
        except exceptions.ConnectionError:
            self.logged_in = False
            return {}

    def disconnect(self):
        self.logged_in = False
        return self._request(
            'logout'
        )

    #****************************************************************
    # Functions to access UniFi controller API routes from here:
    #****************************************************************

    def authorize_guest(self, mac, minutes, up=None, down=None, mbytes=None, ap_mac=None):
        """
        Authorize a guest based on his MAC address.

        Args:
            mac: the guest MAC address
            minutes: duration of the authorization in minutes
            up: up speed allowed in kbps (optional)
            down: down speed allowed in kbps (optional)
            byte: quantity of bytes allowed in MB (optional)
            ap_mac: access point MAC address (UniFi >= 3.x) (optional)
        Returns:
            Response object
        """

        data = {
            'cmd': 'authorize-guest',
            'mac': mac, 
            'minutes': minutes
        }

        if up is not None:
            data['up'] = up
        if down is not None:
            data['down'] = down
        if bytes is not None:
            data['bytes'] = mbytes
        if ap_mac is not None and self.version != 'v2':
            data['ap_mac'] = ap_mac

        return self._request(
            'cmd/stamgr',
            data
        )

    def unauthorize_guest(self, mac):
        """
        Unauthorize a guest based on his MAC address.
        
        mac: the guest MAC address
        """

        return self._request(
            'cmd/stamgr',
            {
                'cmd': 'unauthorize-guest',
                'mac': mac
            }
        )

    def reconnect_sta(self, mac):
        """
        Reconnect a client device

        mac: the guest MAC address
        """

        return self._request(
            'cmd/stamgr',
            {
                'cmd': 'kick-sta',
                'mac': mac
            }
        )

    def block_sta(self, mac):
        """
        Block a client device

        mac: the guest MAC address
        """

        return self._request(
            'cmd/stamgr',
            {
                'cmd': 'block-sta',
                'mac': mac
            }
        )

    def unblock_sta(self, mac):
        """
        Unblock a client device

        mac: the guest MAC address
        """

        return self._request(
            'cmd/stamgr',
            {
                'cmd': 'unblock-sta',
                'mac': mac
            }
        )

    def forget_sta(self, macs):
        """
        Forget one or more client devices

        macs: array of client MAC addresses
        """

        return self._request(
            'cmd/stamgr',
            {
                'cmd': 'forget-sta',
                'macs': macs
            }
        )

    def get_events(self):
        """Return a list of all Events."""

        return self._request(
            'stat/event'
        )

    def get_aps(self):
        """Return a list of all AP:s, with significant information about each."""
        
        return self._request(
            'stat/device',
            {
                '_depth': 2, 
                'test': 0
            }
        )

    def get_clients(self):
        """Return a list of all active clients, with significant information about each."""

        return self._request(
            'stat/sta'
        )

    def get_users(self):
        """Return a list of all known clients, with significant information about each."""

        return self._request(
            'list/user'
        )

    def get_user_groups(self):
        """Return a list of user groups with its rate limiting settings."""

        return self._request(
            'list/usergroup'
        )

    def get_wlan_conf(self):
        """Return a list of configured WLANs with their configuration parameters."""

        return self._request(
            'list/wlanconf'
        )