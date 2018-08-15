import requests
import json
import logging
from urllib.parse import quote_plus
from common_helper_files.fail_safe_file_operations import get_binary_from_file


def _make_search_request(host, search_query, rest_endpoint):
    url = '{}{}{}'.format(host, rest_endpoint, quote_plus(search_query))
    try:
        search_result_json = requests.get(url).json()
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError, json.JSONDecodeError) as e:
        logging.error('Error: %s' % e)
        exit(1)
    if 'error_message' in search_result_json:
        logging.error('[ERROR] {}'.format(search_result_json['error_message']))
        exit(1)
    return search_result_json


def make_search_request_file(host, search_query):
    return _make_search_request(host, search_query, '/rest/file_object?query=')


def make_search_request_firmware(host, search_query):
    return _make_search_request(host, search_query, '/rest/firmware?recursive=true&query=')


def get_and_validate_query(query, query_file):
    if query is not None:
        search_query = query
    elif query_file is not None:
        search_query = get_binary_from_file(query_file).decode('utf-8', 'ignore')
    else:
        raise RuntimeError('No query given. Please specify a query with -q or -Q option')
    logging.debug('Search query is: ', search_query)
    json.loads(search_query)
    return search_query
