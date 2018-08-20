import requests
import json
import logging
from urllib.parse import quote_plus
from common_helper_files.fail_safe_file_operations import get_binary_from_file


def _make_search_request(host, search_query, rest_endpoint):
    url = '{}{}{}'.format(host, rest_endpoint, quote_plus(search_query))
    search_result_json = requests.get(url).json()
    if 'error_message' in search_result_json:
        raise RuntimeError(search_result_json['error_message'])
    return search_result_json


def make_search_request_file(host, search_query):
    return _make_search_request(host, search_query, '/rest/file_object?query=')


def make_search_request_firmware(host, search_query):
    return _make_search_request(host, search_query, '/rest/firmware?recursive=true&query=')


def _get_query(query, query_file):
    if query is not None:
        search_query = query
    elif query_file is not None:
        search_query = get_binary_from_file(query_file).decode('utf-8', 'ignore')
    else:
        raise RuntimeError('No query given. Please specify a query with -q or -Q option')
    logging.debug('Search query is: {}'.format(search_query))
    return search_query


def _validate_query(query_string):
    json.loads(query_string)


def get_and_validate_query(query, query_file):
    search_query = _get_query(query, query_file)
    _validate_query(search_query)
    return search_query
