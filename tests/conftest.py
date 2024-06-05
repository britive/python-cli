import json
import os
from pathlib import Path
from click.testing import CliRunner
import pytest
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
    prepare = os.getenv('PYBRITIVE_PREPARE_DOT_BRITIVE', 'false')
    if prepare == 'true':
        local_home = os.getenv('PYBRITIVE_HOME_DIR')
        if home:
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


def home():
    h = Path(os.getenv('PYBRITIVE_HOME_DIR', '~'))
    return str(h)


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return cli_interface.cli


@pytest.fixture
def profile():
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.cache')
    profiles = []
    while not profiles:
        with open(str(path), 'r', encoding="utf-8") as f:
            loaded_profiles = json.loads(f.read()).get('profiles')
        if not loaded_profiles:
            runner.invoke(cli, 'cache profiles'.split(' '))
            continue
        profiles += loaded_profiles
    return [p for p in loaded_profiles if 'AWS' in p][-1]


@pytest.fixture
def unset_api_token_env_var():
    name = 'BRITIVE_API_TOKEN'
    if name in os.environ:
        del os.environ[name]
