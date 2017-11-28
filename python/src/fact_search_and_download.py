#!/usr/bin/env python3

import base64
import json
import requests
import getpass
import sys
from urllib.parse import quote_plus

host = 'https://faf.caad.fkie.fraunhofer.de'
username = ''
search_query = ''


def check_arguments():
    arg_index = 0
    global host
    global username
    global search_query
    for arg in sys.argv:
        arg_index += 1
        if arg == '-h' or arg == '--help':
            print("This program is used to search for images in the FACT database, and download all images matching the search query.\n"
                  "Use these arguments to modify your search:\n"
                  "-h or --help: display this help\n"
                  "-H [Host] or --host [Host]: change the host. Default: https://faf.caad.fkie.fraunhofer.de\n"
                  "-u [Username] or --user [Username]\n"
                  "-q [json-string] or --query [json-string]: a search query as a string\n"
                  "-Q [json-file] or --queryfile [json-file]: a search query in a .json file")
            raise SystemExit
        elif arg == '-H' or arg == '--host':
            host = sys.argv[arg_index]
        elif arg == '-u' or arg == '--user':
            username = sys.argv[arg_index]
            print("Username: ", username)
        elif arg == '-q' or arg == '--query':
            search_query = sys.argv[arg_index]
        elif arg == '-Q' or arg == '--queryfile':
            with open(sys.argv[arg_index]) as query_file:
                search_query = query_file.read()


def get_search_query():
    global search_query
    if not search_query:
        search_query = input("Please enter your search query: ")
    try:
        json.loads(search_query)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None
    print("Search query is: ", search_query)
    return search_query


def get_user():
    global username
    if not username:
        username = input("Enter your username: ")


def make_search_request_firmware(password):
    url = '{}{}{}'.format(host, '/rest/firmware?query=', quote_plus(search_query))
    search_result_json = requests.get(url, auth=(username, password))
    print("Search for firmware returned status-code ", search_result_json.status_code)
    return search_result_json


def make_search_request_file_object(password):
    url = '{}{}{}'.format(host, '/rest/file_object?query=', quote_plus(search_query))
    search_result_json = requests.get(url, auth=(username, password))
    print("Search for file returned status-code ", search_result_json.status_code)
    return search_result_json


def make_download_request(firmware_uid, password):
    url = '{}{}{}'.format(host, '/rest/binary/', str(firmware_uid))
    download_json = requests.get(url, auth=(username, password))
    print("Download returned status-code ", download_json.status_code)
    return download_json


def download_found_image(firmware_uid, password):
    print("Downloading image with id ", firmware_uid)
    download_json = make_download_request(firmware_uid, password)
    firmware_file_name = download_json.json()['file_name']
    print("File name: ", firmware_file_name)
    binary_base64 = download_json.json()['binary']
    binary = base64.b64decode(binary_base64)
    with open(firmware_file_name, 'wb') as downloaded_file:
        downloaded_file.write(binary)


def get_parent_uids_from_file_object(file_object_uid, password):
    url = '{}{}{}'.format(host, '/rest/file_object/', quote_plus(file_object_uid))
    test = requests.get(url, auth=(username, password))
    file_object = test.json()['file_object']
    firmwares_including_this_file = []
    for key, value in file_object.items():
        nested = file_object[key]
        for key2, value2 in nested.items():
            if key2 == 'firmwares_including_this_file':
                firmwares_including_this_file = value2
    return firmwares_including_this_file


def compare_with_file_objects(firmware_uids, password):
    search_file_object_result = make_search_request_file_object(password)
    all_unique_uids = []
    for uid in search_file_object_result.json()['uids']:
        parent_uids = get_parent_uids_from_file_object(uid, password)
        for parent_uid in parent_uids:
            if parent_uid not in all_unique_uids:
                all_unique_uids.append(parent_uid)
    for firmware_uid in firmware_uids:
        if firmware_uid not in all_unique_uids:
            all_unique_uids.append(firmware_uid)
    return all_unique_uids


def main():
    check_arguments()
    get_user()
    password = getpass.getpass()
    get_search_query()
    search_result_json = make_search_request_firmware(password)
    firmware_uids_complete = compare_with_file_objects(search_result_json.json()['uids'], password)

    downloaded_images = 0
    for firmware_uid in firmware_uids_complete:
        download_found_image(firmware_uid, username, password)
        downloaded_images = downloaded_images + 1
    print("Found {} image(s), downloaded {} image(s)".format(len(firmware_uids_complete), downloaded_images))


if __name__ == "__main__":
    main()
