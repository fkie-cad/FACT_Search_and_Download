import pytest
from pathlib import Path
from common_helper_process import execute_shell_command_get_return_code

SRC_DIR = Path(__file__).parent.parent.parent
MAINSCRIPT = Path(SRC_DIR, 'fact_search_and_download.py')


@pytest.mark.parametrize('function, expected_in_output, expected_return_code', [
    ('-h', 'usage: fact_search_and_download.py', 0),
    ('-V', 'FACT Search and Download', 0),
])
def test_help(function, expected_in_output, expected_return_code):
        output, return_code = execute_shell_command_get_return_code('{} {}'.format(MAINSCRIPT, function), timeout=5)
        assert return_code == expected_return_code
        assert expected_in_output in output
