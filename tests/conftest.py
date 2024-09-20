import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from pybritive import cli_interface


def rm_tree(pth: Path):
    try:
        for child in pth.iterdir():
            if child.is_file():
                child.unlink()
            else:
                rm_tree(child)
        pth.rmdir()
    except FileNotFoundError:
        pass


def prepare_dot_britive():
    if os.getenv('PYBRITIVE_PREPARE_DOT_BRITIVE') == 'true' and (local_home := os.getenv('PYBRITIVE_HOME_DIR')):
        rm_tree(Path(local_home) / '.britive')


def pytest_sessionstart():
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print('pytest_sessionstart')
    prepare_dot_britive()


def pytest_sessionfinish():
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    print('\n\npytest_sessionfinish')
    prepare_dot_britive()


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return cli_interface.cli


@pytest.fixture
def unset_api_token_env_var():
    if os.getenv((name := 'BRITIVE_API_TOKEN')):
        del os.environ[name]
