import os

PROFILE = os.getenv('PYBRITIVE_TEST_PROFILE')


def test_checkin(runner, cli):
    result = runner.invoke(cli, ['checkin', PROFILE])
    assert result.exit_code == 0
    assert result.output == ''
