#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


class APIError(Exception):
    pass

class CredentialsMissing(Exception):
    """ username or password are missing. """

class ConnectionError(Exception):
    pass