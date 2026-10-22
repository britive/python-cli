def common_asserts(result, substring=None, exit_code=0):
    assert result.exit_code == exit_code
    if isinstance(substring, str):
        substring = [substring]
    for sub in substring:
        assert sub in result.output


def test_create(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '-f', 'json', '--silent'])
    common_asserts(result, ['accessToken', 'expiresOn'])


def test_create_with_duration(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '--duration-seconds', '900', '-f', 'json', '--silent'])
    common_asserts(result, ['accessToken', 'expiresOn'])


def test_create_mode_token(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '-m', 'token'])
    common_asserts(result, 'eyJ')
    assert len(result.output.strip().split('.')) == 3


def test_create_mode_decode(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '-m', 'decode', '-f', 'json'])
    common_asserts(result, ['header', 'payload', 'expiresIn'])


def test_create_mode_env(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '-m', 'env-nix'])
    common_asserts(result, ['export BRITIVE_TENANT="https://', 'export BRITIVE_TOKEN="eyJ', 'BRITIVE_TOKEN_EXPIRATION'])


def test_create_mode_env_winps(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '-m', 'env-winps'])
    common_asserts(result, ['$Env:BRITIVE_TENANT=', '$Env:BRITIVE_TOKEN='])


def test_create_mode_clipboard(runner, cli, monkeypatch):
    from pybritive.helpers import clipboard

    copied = []
    monkeypatch.setattr(clipboard.shutil, 'which', lambda cmd: cmd)
    monkeypatch.setattr(clipboard.subprocess, 'run', lambda cmd, **kwargs: copied.append(kwargs['input']))
    result = runner.invoke(cli, ['tokens', 'create', '-m', 'clipboard'])
    common_asserts(result, 'copied to clipboard')
    assert copied and copied[0].startswith('eyJ')


def test_help(runner, cli):
    result = runner.invoke(cli, ['tokens', '--help'])
    common_asserts(result, ['create', 'get', 'list', 'revoke'])


def test_create_help(runner, cli):
    result = runner.invoke(cli, ['tokens', 'create', '--help'])
    common_asserts(result, ['--duration-seconds', '--mode', '--format', '--tenant', '--token', '--silent'])


def test_list_not_implemented(runner, cli):
    result = runner.invoke(cli, ['tokens', 'list', '--tenant', 'example'])
    common_asserts(result, 'Listing temporary tokens is not yet implemented.', exit_code=1)


def test_get_not_implemented(runner, cli):
    result = runner.invoke(cli, ['tokens', 'get', 'example-id', '--tenant', 'example'])
    common_asserts(result, 'Viewing temporary tokens is not yet implemented.', exit_code=1)


def test_revoke_not_implemented(runner, cli):
    result = runner.invoke(cli, ['tokens', 'revoke', 'example-id', '--tenant', 'example'])
    common_asserts(result, 'Revoking temporary tokens is not yet implemented.', exit_code=1)
