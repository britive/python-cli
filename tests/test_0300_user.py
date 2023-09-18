import os


def test_user(runner, cli):
    result = runner.invoke(cli, ['user'])
    tenant = os.getenv('PYBRITIVE_TEST_TENANT')
    assert f'@ {tenant}' in result.output
