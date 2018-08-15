#!/usr/bin/env python3
'''
    FACT Search and Download
    Copyright (C) 2017-2018  Fraunhofer FKIE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import base64
import json
import requests
from urllib.parse import quote_plus
import argparse
import os
from pathlib import Path

from helper.storage import get_storage_path

PROGRAM_NAME = 'FACT Search and Download'
PROGRAM_VERSION = '0.3'
PROGRAM_DESCRIPTION = 'This program finds and downloads files matching a specific query.'


def check_arguments():
    parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
    parser.add_argument('-V', '--version', action='version', version='{} {}'.format(PROGRAM_NAME, PROGRAM_VERSION))
    parser.add_argument('-H', '--host', help='Change the host', default='http://localhost:5000')
    parser.add_argument('-q', '--query', help='A search query as a string', default=None)
    parser.add_argument('-Q', '--queryfile', help='A search query in a .json file', default=None)
    parser.add_argument('-F', '--firmware', action='store_true', help='download firmwares including files matching the query', default=False)
    parser.add_argument('-d', '--destination', help='store files in this folder', default='.')
    arguments = parser.parse_args()
    return arguments


def get_search_query(arguments):
    search_query = arguments.query
    if not search_query and arguments.queryfile is not None:
        with open(arguments.queryfile) as query_file:
            search_query = query_file.read()
    elif not search_query:
        search_query = input('Please enter your search query: ')
    try:
        json.loads(search_query)
    except ValueError as e:
        print('Invalid json: %s' % e)
        exit(1)
    print('Search query is: ', search_query)
    return search_query


def make_search_request(host, search_query):
    url = '{}{}{}'.format(host, '/rest/file_object?query=', quote_plus(search_query))
    try:
        search_result_json = requests.get(url).json()
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError, json.JSONDecodeError) as e:
        print('Error: %s' % e)
        exit(1)
    if 'error_message' in search_result_json:
        print('[ERROR] {}'.format(search_result_json['error_message']))
        exit(1)
    return search_result_json


def make_search_request_firmware(host, search_query):
    url = '{}{}{}'.format(host, '/rest/firmware?recursive=true&query=', quote_plus(search_query))
    try:
        search_result_json = requests.get(url).json()
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError, json.JSONDecodeError) as e:
        print('Error: %s' % e)
        exit(1)
    if 'error_message' in search_result_json:
        print('[ERROR] {}'.format(search_result_json['error_message']))
        exit(1)
    return search_result_json


def make_download_request(host, firmware_uid):
    url = '{}{}{}'.format(host, '/rest/binary/', str(firmware_uid))
    try:
        download_json = requests.get(url).json()
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError, json.JSONDecodeError) as e:
        print('Error: %s' % e)
        return None
    return download_json


def download_file(host, file_uid, storage_directory):
    print('Downloading file with uid ', file_uid)
    download_json = make_download_request(host, file_uid)
    if download_json is None:
        return None
    binary_base64 = download_json['binary']
    try:
        binary = base64.b64decode(binary_base64)
    except (TypeError, SyntaxError) as e:
        print('Error: %s' % e)
        return None
    storage_path = get_storage_path(download_json['file_name'], storage_directory)
    with open(storage_path, 'wb') as downloaded_file:
        downloaded_file.write(binary)
    return 0


def append_number_if_duplicate(firmware_file_name):
    index = 0
    new_firmware_file_name = firmware_file_name
    while os.path.isfile(new_firmware_file_name):
        index = index + 1
        new_firmware_file_name = '{}({})'.format(firmware_file_name, index)
    return new_firmware_file_name


def main():
    arguments = check_arguments()
    search_query = get_search_query(arguments)
    host = arguments.host
    storage_directory = Path(arguments.destination)
    storage_directory.mkdir(parents=True, exist_ok=True)
    if arguments.firmware:
        search_result_json = make_search_request_firmware(host, search_query)
    else:
        search_result_json = make_search_request(host, search_query)
    downloaded_files = 0
    for firmware_uid in search_result_json['uids']:
        if download_file(host, firmware_uid, storage_directory) is not None:
            downloaded_files = downloaded_files + 1
    print('Found {} files(s), downloaded {} files(s)'.format(len(search_result_json.json()['uids']), downloaded_files))
    return 0


if __name__ == '__main__':
    exit(main())
