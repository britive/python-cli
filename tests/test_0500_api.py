def common_asserts(result, substring=None, exit_code=0):
    assert result.exit_code == exit_code
    if isinstance(substring, str):
        substring = [substring]
    for sub in substring:
        assert sub in result.output


def test_api(runner, cli):
    result = runner.invoke(cli, 'api users.list'.split(' '))
    common_asserts(result, ['userId', 'status', 'email', 'identityProvider'])
