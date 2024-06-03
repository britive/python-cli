def test_checkin(runner, cli, profile):
    result = runner.invoke(cli, ['checkin', profile])
    assert result.exit_code == 0
    assert result.output == ''
