import pytest
from click.testing import CliRunner
from pybritive import cli_interface


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli():
    return cli_interface.cli

