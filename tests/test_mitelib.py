# -*- coding: utf-8 -*-
# File: test_mitelib.py
""" test module to test the mite library wrapper. """

__author__ = 'Otto Hockel <hockel.otto@googlemail.com>'
__docformat__ = 'plaintext'

import pytest
import json
import urllib.request
from .conftest import mock_urlopen, mock_http_error
from pymite.adapters import DefaultReadAdapter


def test_setup(libfactory):
    assert libfactory is not None


def test_factory_properties(libfactory):
    assert libfactory._apikey == 'bar'
    assert libfactory._realm == 'foo'
    adapters = ['tracker', 'daily', 'users', 'time_entries', 'customers',
                'services', 'projects']
    for adapter in adapters:
        assert libfactory.__getattribute__('%s_adapter' % adapter)


def test_base_api_properties(monkeypatch, base_api):
    """we do not process data except the declassification of some
    top level properties.
    """

    assert base_api.realm == 'foo'
    assert base_api._realm == 'foo'

    assert base_api.apikey == 'bar'
    assert base_api._apikey == 'bar'

    headers = {
        'X-MiteApiKey': 'bar',
        'Content-Type': 'text/json',
        'User-Agent': 'pymite/dev (https://github.com/damnit)'
    }

    assert base_api._headers == headers

    assert base_api._api('baz') == 'https://foo.mite.yo.lk/baz'
    assert base_api.__repr__() == '<mite: MiteAPI Adapter>'


def test_base_api_myself(monkeypatch, base_api):
    """ Test myself adapter property. """
    myself = {'user': {}}

    urlopen_myself = mock_urlopen(myself)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_myself)

    assert base_api.myself == myself['user']


def test_http_get_error(monkeypatch, base_api):
    """ Test myself adapter property. """
    error = {'error': "Whoops! We couldn't find your account 'foo'."}
    urlopen_error = mock_http_error(code=404, message=json.dumps(error))
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_error)
    assert error == base_api.myself


def test_http_post_error(monkeypatch, libfactory):
    """ Test myself adapter property. """
    te = libfactory.time_entries_adapter
    error = {'error': "Whoops! You are not allowed to create an entry."}
    urlopen_error = mock_http_error(code=404, message=json.dumps(error))
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_error)
    assert error == te.create(minutes=42, note='foo', user_id=666)


def test_http_put_error(monkeypatch, libfactory):
    """ Test myself adapter property. """
    error = {'error': "Whoops! We couldn't find the given entry."}
    urlopen_error = mock_http_error(code=404, message=json.dumps(error))
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_error)
    assert error == libfactory.tracker_adapter.start(1)


def test_http_delete_error(monkeypatch, libfactory):
    """ Test myself adapter property. """
    error = {'error': "Whoops! We couldn't find the given entry."}
    urlopen_error = mock_http_error(code=404, message=json.dumps(error))
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_error)
    assert error == libfactory.tracker_adapter.stop(1)


def test_base_api_account(monkeypatch, base_api):
    """ Test account adapter property. """
    account = {'account': {}}

    urlopen_account = mock_urlopen(account)
    monkeypatch.setattr(urllib.request, 'urlopen', urlopen_account)

    assert base_api.account == account['account']


def test_default_adapter_constructor(monkeypatch, base_api):
    """ the setup of the rather virtual default read adapter. """
    with pytest.raises(TypeError):
        DefaultReadAdapter(base_api.realm, base_api.apikey)

# vim: set ft=python ts=4 sw=4 expandtab :
