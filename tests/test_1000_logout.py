from pathlib import Path
import os


def test_logout(runner, cli, profile):
    result = runner.invoke(cli, ['logout'])
    assert result.exit_code == 0
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.credentials')
    with open(str(path), 'r') as f:
        data = f.read()
    assert len(data) == 0





