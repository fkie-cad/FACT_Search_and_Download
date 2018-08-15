import pytest
from pathlib import Path
from helper.storage import get_storage_path


STORAGE_DIR = Path(Path(__file__).parent.parent.parent, 'data')


@pytest.mark.parametrize('file_name, expected_output', [
    ('none_existing', 'none_existing'),
    ('existing', 'existing-0'),
    ('existing-twice', 'existing-twice-1')
])
def test_get_storage_path(file_name, expected_output):
    print(STORAGE_DIR)
    designated_path = Path(STORAGE_DIR, file_name)
    expected_resulting_path = Path(STORAGE_DIR, expected_output)
    assert get_storage_path(designated_path, STORAGE_DIR) == expected_resulting_path
