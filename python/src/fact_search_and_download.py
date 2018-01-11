#!/usr/bin/env python3

import base64
import json
import requests
import getpass
import sys
from urllib.parse import quote_plus
import argparse
import os


def check_arguments():
    parser = argparse.ArgumentParser(description='This program is used to search for images in the FACT database, '
                                                 'and download all images matching the search query.')
    parser.add_argument('-H', '--host', help='Change the host',
                        default='https://faf.caad.fkie.fraunhofer.de')
    parser.add_argument('-u', '--user', help='State your username', default=None)
    parser.add_argument('-q', '--query', help='A search query as a string', default=None)
    parser.add_argument('-Q', '--queryfile', help='A search query in a .json file', default=None)
    arguments = parser.parse_args()
    return arguments


def get_user(username):
    if not username:
        username = input("Enter your username: ")
    return username


def get_search_query(arguments):
    search_query = arguments.query
    if not search_query and arguments.queryfile is not None:
        with open(arguments.queryfile) as query_file:
            search_query = query_file.read()
    elif not search_query:
        search_query = input("Please enter your search query: ")
    try:
        json.loads(search_query)
    except ValueError as e:
        print('Invalid json: %s' % e)
        exit(1)
    print("Search query is: ", search_query)
    return search_query


def make_search_request_firmware(username, password, host, search_query):
    url = '{}{}{}'.format(host, '/rest/firmware?recursive=true&query=', quote_plus(search_query))
    try:
        search_result_json = requests.get(url, auth=(username, password))
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError) as e:
        print('Error: %s' % e)
        exit(1)
    return search_result_json


def make_download_request(username, password, host, firmware_uid):
    url = '{}{}{}'.format(host, '/rest/binary/', str(firmware_uid))
    try:
        download_json = requests.get(url, auth=(username, password))
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError) as e:
        print('Error: %s' % e)
        return None
    return download_json


def download_found_image(username, password, host, firmware_uid):
    print("Downloading image with id ", firmware_uid)
    download_json = make_download_request(username, password, host, firmware_uid)
    try:
        firmware_file_name = append_number_if_duplicate(download_json.json()['file_name'])
    except KeyError:
        print('Error: No download possible. No file found with this id.')
        return None
    print("File name: ", firmware_file_name)
    binary_base64 = download_json.json()['binary']
    try:
        binary = base64.b64decode(binary_base64)
    except (TypeError, SyntaxError) as e:
        print('Error: %s' % e)
        return None
    with open(firmware_file_name, 'wb') as downloaded_file:
        downloaded_file.write(binary)
    return 0


def append_number_if_duplicate(firmware_file_name):
    index = 0
    new_firmware_file_name = firmware_file_name
    while os.path.isfile(new_firmware_file_name):
        index = index + 1
        new_firmware_file_name = "{}({})".format(firmware_file_name, index)
    return new_firmware_file_name


def main():
    arguments = check_arguments()
    username = get_user(arguments.user)
    password = getpass.getpass()
    search_query = get_search_query(arguments)
    host = arguments.host
    search_result_json = make_search_request_firmware(username, password, host, search_query)
    downloaded_images = 0
    for firmware_uid in search_result_json.json()['uids']:
        if download_found_image(username, password, host, firmware_uid) is not None:
            downloaded_images = downloaded_images + 1
    print("Found {} image(s), downloaded {} image(s)".format(len(search_result_json.json()['uids']), downloaded_images))
    return 0


if __name__ == "__main__":
    exit(main())
