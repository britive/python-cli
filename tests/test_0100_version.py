def common_asserts(result):
    assert result.exit_code == 0
    assert 'pybritive:' in result.output
    assert '/ platform:' in result.output
    assert '/ python: 3.' in result.output


def test_version_full_flag(runner, cli):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['--version'])
        common_asserts(result)


def test_version_short_flag(runner, cli):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['-v'])
        common_asserts(result)
