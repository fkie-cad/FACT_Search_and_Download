import json
import tempfile
from pathlib import Path

import requests
from helper.rest_download import _make_download_request, download_file
from helper.storage import get_storage_path


class RequestsGetResponseMock:
    def __init__(self, content):
        self._content = content

    def json(self):
        if self._content == 'not valid':
            raise json.JSONDecodeError('Not valid', self._content, 1)
        return self._content


JSON_ERROR_RESPONSE = RequestsGetResponseMock('not valid')
VALID_JSON_RESPONSE = RequestsGetResponseMock({'binary': 'foo', 'file_name': 'bar'})


def mock_request_exception(url):
    raise requests.RequestException('ds', 'f', 1)


def mock_type_error(s):
    raise TypeError('ds', 'f', 1)


def mock_syntax_error(s):
    raise SyntaxError('ds', 'f', 1)


def test_make_download_request(monkeypatch):
    monkeypatch.setattr('requests.get', lambda url: JSON_ERROR_RESPONSE)
    assert _make_download_request('', '') is None

    monkeypatch.setattr('requests.get', lambda url: VALID_JSON_RESPONSE)
    assert _make_download_request('', '') == VALID_JSON_RESPONSE.json()

    # All exceptions that Requests explicitly raises inherit from requests.exceptions.RequestException
    monkeypatch.setattr('requests.get', mock_request_exception)
    assert _make_download_request('', '') is None


def test_download_file_error(monkeypatch):
    monkeypatch.setattr('requests.get', lambda url: JSON_ERROR_RESPONSE)
    assert download_file('', '', '') is None

    monkeypatch.setattr('requests.get', lambda url: VALID_JSON_RESPONSE)
    monkeypatch.setattr('base64.b64decode', mock_syntax_error)
    assert download_file('', '', '') is None

    monkeypatch.setattr('requests.get', lambda url: VALID_JSON_RESPONSE)
    monkeypatch.setattr('base64.b64decode', mock_type_error)
    assert download_file('', '', '') is None


def test_download_file_valid(monkeypatch):
    download_json = VALID_JSON_RESPONSE.json()
    monkeypatch.setattr('requests.get', lambda url: VALID_JSON_RESPONSE)
    binary = bytes(download_json['binary'], encoding='utf-8')
    monkeypatch.setattr('base64.b64decode', lambda binary_base64: binary)

    temp_dir = tempfile.TemporaryDirectory()
    storage_path = get_storage_path(download_json['file_name'], temp_dir.name)

    assert download_file('', '', temp_dir.name) == 0
    assert_file_is_correctly_written(storage_path, download_json)

    temp_dir.cleanup()


def assert_file_is_correctly_written(storage_path, download_json):
    is_file = Path(storage_path).is_file()
    assert is_file

    if is_file:
        with open(str(storage_path), 'r') as downloaded_file:
            c = downloaded_file.read()
        assert c == download_json['binary']
