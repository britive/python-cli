from pathlib import Path


def common_asserts(result, substring=None, exit_code=0):
    assert result.exit_code == exit_code
    if isinstance(substring, str):
        substring = [substring]
    for sub in substring:
        assert sub in result.output


def test_view(runner, cli):
    result = runner.invoke(cli, 'secret view /pybritive-test-standard -f yaml'.split(' '))
    common_asserts(result, 'test')


def test_download(runner, cli):
    filename = 'pybritive-test-secret-file.txt'
    result = runner.invoke(cli, 'secret download /pybritive-test-file'.split(' '))
    message = 'wrote contents of secret file to'
    common_asserts(result, message)
    with open(filename, encoding='utf-8') as f:
        assert 'test' in f.read()
    path = Path(filename)
    path.unlink(missing_ok=True)


def test_download_filename_provided(runner, cli):
    filename = 'pybritive-test-secret-file-2.txt'
    result = runner.invoke(cli, f'secret download /pybritive-test-file -F {filename}'.split(' '))
    message = 'wrote contents of secret file to'
    common_asserts(result, message)
    with open(filename, encoding='utf-8') as f:
        assert 'test' in f.read()
    path = Path(filename)
    path.unlink(missing_ok=True)
