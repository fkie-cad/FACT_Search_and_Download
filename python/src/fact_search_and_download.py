#!/usr/bin/env python3

import base64
import json
import requests
import getpass
from urllib.parse import quote_plus

def get_search_query():
    data = input("Please enter your search query: ")
    try:
        json.loads(data)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None
    print ("Search query is: ", data)
    return data

def make_search_request(data, username, password):
    url = '{}{}{}'.format('https://faf.caad.fkie.fraunhofer.de/rest/firmware?query=', quote_plus(data), '&firmware_flag=True')
    search_result_json = requests.get(url, auth=(username, password))
    print ("Search returned status-code ", search_result_json.status_code)
    return search_result_json

def make_download_request(firmware_uid, username, password):
    url = '{}{}'.format('https://faf.caad.fkie.fraunhofer.de/rest/binary/', str(firmware_uid))
    download_json = requests.get(url, auth=(username, password))
    print ("Download returned status-code ", download_json.status_code)
    return download_json

def download_found_image(firmware_uid, username, password):
    print ("Downloading image with id ", firmware_uid)
    download_json = make_download_request(firmware_uid, username, password)
    firmware_file_name = download_json.json()['file_name']
    print ("File name: ", firmware_file_name)
    binary_base64 = download_json.json()['binary']
    binary = base64.b64decode(binary_base64)
    with open(firmware_file_name, 'wb') as downloaded_file:
        downloaded_file.write(binary)

if __name__ == "__main__":
    username = input("Enter your username: ")
    password = getpass.getpass()
    data = get_search_query()
    search_result_json = make_search_request(data, username, password)

    count_firmware_images = 0
    for firmware_uid in search_result_json.json()['uids']:
        download_found_image(firmware_uid, username, password)
        count_firmware_images = count_firmware_images+1
    print ("Downloaded {} image(s)".format(count_firmware_images))
