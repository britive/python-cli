def common_asserts(result, substring=None, exit_code=0):
    assert result.exit_code == exit_code
    if isinstance(substring, str):
        substring = [substring]
    for sub in substring:
        assert sub in result.output


def test_ls_profiles(runner, cli):
    result = runner.invoke(cli, 'ls profiles -f yaml'.split(' '))
    common_asserts(result, ['Application', 'Description', 'Environment', 'Profile', 'Type'])


def test_ls_applications(runner, cli):
    result = runner.invoke(cli, 'ls applications -f yaml'.split(' '))
    common_asserts(result, ['Application', 'Description', 'Type'])


def test_ls_environments(runner, cli):
    result = runner.invoke(cli, 'ls environments -f yaml'.split(' '))
    common_asserts(result, ['Application', 'Description', 'Environment', 'Type'])


def test_ls_secrets(runner, cli):
    result = runner.invoke(cli, 'ls secrets -f yaml'.split(' '))
    common_asserts(
        result,
        ['entityType', 'id', 'metadata', 'name', 'path', 'rotationInterval', 'secretNature', 'secretType', 'status'],
    )
