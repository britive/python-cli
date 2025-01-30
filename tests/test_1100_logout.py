import os
from pathlib import Path


def test_logout(runner, cli):
    result = runner.invoke(cli, ['logout'])
    assert result.exit_code == 0
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.credentials.encrypted')
    with open(str(path), encoding='utf-8') as f:
        data = f.read()
    assert len(data) == 0
