import os
import warnings
from pathlib import Path


def test_login_interactive(runner, cli):
    result = runner.invoke(cli, 'login')
    api_login_warning = 'Interactive login unavailable when an API token is provided.'
    if api_login_warning in result.output:
        warnings.warn(api_login_warning.upper(), stacklevel=2)
        return
    assert result.exit_code == 0
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.credentials.encrypted')
    with open(str(path), encoding='utf-8') as f:
        data = f.read()
    assert 'accessToken=' in data
    assert os.getenv('PYBRITIVE_TEST_TENANT') in data


def test_user(runner, cli):
    result = runner.invoke(cli, 'user')
    tenant = os.getenv('PYBRITIVE_TEST_TENANT')
    assert f'@ {tenant}' in result.output
