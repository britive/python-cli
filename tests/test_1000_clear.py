import json
import os
from pathlib import Path


def test_clear_cache(runner, cli):
    result = runner.invoke(cli, 'clear cache'.split(' '))
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(Path(local_home) / '.britive' / 'pybritive.cache')
    with open(str(path), encoding='utf-8') as f:
        data = json.loads(f.read())
    assert result.exit_code == 0
    assert 'profiles' in data
    assert len(data['profiles']) == 0


def test_clear_gcloud_key_files(runner, cli):
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    path = Path(local_home) / '.britive' / 'pybritive-gcloud-key-files'
    file1 = path / 'file1.json'
    file2 = path / 'file2.json'

    path.mkdir(exist_ok=True, parents=True)
    file1.write_text('')
    file2.write_text('')

    assert path.is_dir()
    assert file1.is_file()
    assert file2.is_file()

    result = runner.invoke(cli, 'clear gcloud-auth-key-files'.split(' '))
    assert result.exit_code == 0
    assert not file1.is_file()
    assert not file2.is_file()
    assert not path.is_dir()
