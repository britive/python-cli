import os
from pathlib import Path
import json


def test_cache_profiles(runner, cli):
    result = runner.invoke(cli, 'cache profiles'.split(' '))
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.cache')
    with open(str(path), 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    assert result.exit_code == 0
    assert 'profiles' in data.keys()
    assert len(data['profiles']) > 0
    assert len(data['profiles'][0].split('/')) in [2, 3]
