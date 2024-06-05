from pathlib import Path
import os
import warnings


def test_login_interactive(runner, cli):
    result = runner.invoke(cli, ['login'])
    api_login_warning = 'Interactive login unavailable when an API token is provided.'
    if api_login_warning in result.output:
        warnings.warn(api_login_warning.upper())
        return
    assert result.exit_code == 0
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.credentials.encrypted')
    with open(str(path), 'r', encoding='utf-8') as f:
        data = f.read()
    assert 'accessToken=' in data
    assert os.getenv('PYBRITIVE_TEST_TENANT') in data
