
def test_checkout_json(runner, cli, profile):
    result = runner.invoke(cli, ['checkin', profile])
    assert result.exit_code == 0
    assert result.output == ''




