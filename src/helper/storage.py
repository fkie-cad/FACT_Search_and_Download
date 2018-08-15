from pathlib import Path


def get_storage_path(file_name, storage_directory):
    index = 0
    storage_path = Path(storage_directory, file_name)
    while storage_path.exists():
        storage_path = Path(storage_directory, '{}-{}'.format(file_name, index))
        index += 1
    return storage_path
