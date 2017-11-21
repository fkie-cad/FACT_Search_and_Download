#!/usr/bin/env python3

import base64
import json
import requests
import getpass
import sys
from urllib.parse import quote_plus

default_host = 'https://faf.caad.fkie.fraunhofer.de'


def get_search_query():
    data = input("Please enter your search query: ")
    try:
        json.loads(data)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None
    print("Search query is: ", data)
    return data


def get_user():
    arg_index = 0
    username = ""
    for arg in sys.argv:
        # print (arg, sys.argv[arg_index])
        arg_index += 1
        if arg == '-u':
            username = sys.argv[arg_index]
            print("Username: ", username)
    if not username:
        username = input("Enter your username: ")
    return username


def make_search_request_firmware(data, username, password):
    url = '{}{}{}'.format(default_host, '/rest/firmware?query=', quote_plus(data))
    search_result_json = requests.get(url, auth=(username, password))
    print("Search returned status-code ", search_result_json.status_code)
    return search_result_json


def make_search_request_file_object(data, username, password):
    url = '{}{}{}'.format(default_host, '/rest/file_object?query=', quote_plus(data))
    search_result_json = requests.get(url, auth=(username, password))
    print("Search returned status-code ", search_result_json.status_code)
    return search_result_json


def make_download_request(firmware_uid, username, password):
    url = '{}{}{}'.format(default_host, '/rest/binary/', str(firmware_uid))
    download_json = requests.get(url, auth=(username, password))
    print("Download returned status-code ", download_json.status_code)
    return download_json


def download_found_image(firmware_uid, username, password):
    print("Downloading image with id ", firmware_uid)
    download_json = make_download_request(firmware_uid, username, password)
    firmware_file_name = download_json.json()['file_name']
    print("File name: ", firmware_file_name)
    binary_base64 = download_json.json()['binary']
    binary = base64.b64decode(binary_base64)
    with open(firmware_file_name, 'wb') as downloaded_file:
        downloaded_file.write(binary)


def get_parent_uids_from_file_object(file_object_uid, username, password):
    url = '{}{}{}'.format(default_host, '/rest/file_object/', quote_plus(file_object_uid))
    test = requests.get(url, auth=(username, password))
    file_object = test.json()['file_object']
    firmwares_including_this_file = []
    virtual_file_path = []
    for key, value in file_object.items():
        # print (key)
        nested = file_object[key]
        for key2, value2 in nested.items():
            # print ('    ', key2)
            if key2 == 'virtual_file_path':
                virtual_file_path=value2
                print('    ', virtual_file_path)
            if key2 == 'firmwares_including_this_file':
                firmwares_including_this_file=value2
                print('There are {} uids'.format(len(firmwares_including_this_file)), '\n', firmwares_including_this_file)


def compare_with_file_object(firmware_uids, data, username, password):
    search_file_object_result = make_search_request_file_object(data, username, password)
    test_uid=search_file_object_result.json()['uids'][0]
    get_parent_uids_from_file_object(test_uid, username, password)
    #for uid in search_file_object_result['uids']:
    #    get_parent_uids_from_file_object(uid, username, password)


def main():
    username = get_user()
    # print ("2: ", username)
    password = getpass.getpass()
    data = get_search_query()
    search_result_json = make_search_request_firmware(data, username, password)
    firmware_uids_complete = compare_with_file_object(search_result_json.json()['uids'], data, username, password)

    count_firmware_images = 0
    for firmware_uid in search_result_json.json()['uids']:
        # download_found_image(firmware_uid, username, password)
        count_firmware_images = count_firmware_images + 1
    print("Downloaded {} image(s)".format(count_firmware_images))


if __name__ == "__main__":
    main()
