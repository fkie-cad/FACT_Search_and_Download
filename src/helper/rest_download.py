import requests
import json
import base64
import logging

from helper.storage import get_storage_path


def _make_download_request(host, firmware_uid):
    url = '{}{}{}'.format(host, '/rest/binary/', str(firmware_uid))
    try:
        download_json = requests.get(url).json()
    except (requests.RequestException, requests.HTTPError, requests.ConnectionError, json.JSONDecodeError) as e:
        logging.error('Error: %s' % e)
        return None
    return download_json


def download_file(host, file_uid, storage_directory):
    logging.debug('Downloading file with uid {}'.format(file_uid))
    download_json = _make_download_request(host, file_uid)
    if download_json is None:
        return None
    binary_base64 = download_json['binary']
    try:
        binary = base64.b64decode(binary_base64)
    except (TypeError, SyntaxError) as e:
        logging.error('Error: %s' % e)
        return None
    storage_path = get_storage_path(download_json['file_name'], storage_directory)
    with open(str(storage_path), 'wb') as downloaded_file:
        downloaded_file.write(binary)
    return 0
