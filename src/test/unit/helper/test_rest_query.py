from helper.rest_query import _make_search_request, make_search_request_file, make_search_request_firmware, get_and_validate_query
import pytest
import json


class MockResponse:
    def __init__(self, content):
        self._content = content

    def json(self):
        return self._content


GOOD_RESPONSE = MockResponse({})
BAD_RESPONSE = MockResponse({'error_message': 'Yay, that\'s patching'})


def test_make_search_request(monkeypatch):
    monkeypatch.setattr('requests.get', lambda url: GOOD_RESPONSE)
    assert 'error_message' not in _make_search_request('', '', '')

    monkeypatch.setattr('requests.get', lambda url: BAD_RESPONSE)
    with pytest.raises(RuntimeError):
        _make_search_request('', '', '')


def test_make_search_request_wrappers(monkeypatch):
    monkeypatch.setattr('requests.get', lambda url: GOOD_RESPONSE)

    assert 'error_message' not in make_search_request_file('', '')
    assert 'error_message' not in make_search_request_firmware('', '')


def test_get_and_validate_query_error():
    with pytest.raises(RuntimeError):
        get_and_validate_query(None, None)


def test_get_and_validate_query_string():
    query_string = '{"foo": "bar"}'
    result = get_and_validate_query(query_string, None)
    assert query_string == result


def test_get_and_validate_raises():
    with pytest.raises(json.JSONDecodeError):
        get_and_validate_query('{\'foo\': \'bar\'}', None)


@pytest.mark.skip(reason='patch not working')
def test_get_and_validate_file(monkeypatch):
    query_string = b'{"foo": "bar"}'
    monkeypatch.setattr('common_helper_files.fail_safe_file_operations.get_binary_from_file', lambda file_path: query_string)
    assert get_and_validate_query(None, '/any/path') == query_string.decode('utf-8', 'ignore')
