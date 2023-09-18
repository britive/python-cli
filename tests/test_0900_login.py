from pathlib import Path
import os


def test_login_when_api_token_present(runner, cli):
    result = runner.invoke(cli, ['login'])
    assert result.exit_code == 1
    assert result.output == 'Error: Interactive login unavailable when an API token is provided.\n'


def test_login_interactive(runner, cli, unset_api_token_env_var):
    result = runner.invoke(cli, ['login'])
    assert result.exit_code == 0
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.credentials.encrypted')
    with open(str(path), 'r') as f:
        data = f.read()
    assert 'accessToken=' in data
    assert os.getenv('PYBRITIVE_TEST_TENANT') in data
