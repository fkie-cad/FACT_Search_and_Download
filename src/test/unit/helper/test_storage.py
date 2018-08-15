import pytest
from pathlib import Path
from helper.storage import get_storage_path, prepare_storage_dir
from tempfile import TemporaryDirectory


STORAGE_DIR = Path(Path(__file__).parent.parent.parent, 'data')


@pytest.mark.parametrize('file_name, expected_output', [
    ('none_existing', 'none_existing'),
    ('existing', 'existing-0'),
    ('existing-twice', 'existing-twice-1')
])
def test_get_storage_path(file_name, expected_output):
    designated_path = Path(STORAGE_DIR, file_name)
    expected_resulting_path = Path(STORAGE_DIR, expected_output)
    assert get_storage_path(designated_path, STORAGE_DIR) == expected_resulting_path


@pytest.mark.parametrize('path', [
    (''),
    ('none_existing'),
])
def test_prepare_storage_dir(path):
    tmp_dir = TemporaryDirectory(prefix='fact_sd_test_')
    storage_destination = '{}/{}'.format(tmp_dir.name, path)
    storage_directory = prepare_storage_dir(storage_destination)
    assert storage_directory.exists()
    assert storage_directory.is_dir()
