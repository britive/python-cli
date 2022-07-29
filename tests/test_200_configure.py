from pathlib import Path


def test_configure_tenant_via_flags(runner, cli, tmp_path):
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['configure', 'tenant', '-t test', '-f yaml'])
        with open(f'{str(Path.home())}/.britive/pybritive.config', 'r') as f:
            data = f.read()
        # assert result.exit_code == 0
        assert '[tenant-test]' in data




