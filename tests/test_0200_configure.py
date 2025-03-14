import os
from typing import Optional


def read_config():
    local_home = os.getenv('PYBRITIVE_HOME_DIR')
    with open(f'{local_home}/.britive/pybritive.config', encoding='utf-8') as f:
        return f.read()


def common_asserts(result, substring: Optional[list] = None, exit_code: int = 0):
    assert result.exit_code == exit_code
    if substring:
        if isinstance(substring, str):
            substring = [substring]
        data = read_config()
        for sub in substring:
            assert sub in data


def test_configure_tenant_via_flags_no_alias(runner, cli):
    result = runner.invoke(cli, 'configure tenant -t pybritivetest1.dev -f yaml'.split(' '))
    common_asserts(result, substring='[tenant-pybritivetest1.dev]')


def test_configure_tenant_via_flags_no_alias_no_format(runner, cli):
    result = runner.invoke(cli, 'configure tenant -t pybritivetest2.dev'.split(' '))
    common_asserts(result, substring='[tenant-pybritivetest2.dev]')


def test_configure_tenant_via_flags_yes_alias(runner, cli):
    result = runner.invoke(cli, 'configure tenant -t pybritivetest1.dev -f yaml -a testalias1'.split(' '))
    common_asserts(result, substring='[tenant-testalias1]')


def test_configure_tenant_via_flags_yes_alias_no_format(runner, cli):
    result = runner.invoke(cli, 'configure tenant -t pybritivetest2.dev -a testalias2'.split(' '))
    common_asserts(result, substring='[tenant-testalias2]')


def test_configure_tenant_via_prompt_no_alias(runner, cli):
    result = runner.invoke(cli, 'configure tenant'.split(' '), input='pybritivetest3.dev\n\njson\n')
    common_asserts(result, substring='[tenant-pybritivetest3.dev]')


def test_configure_tenant_via_prompt_no_alias_no_format(runner, cli):
    result = runner.invoke(cli, 'configure tenant'.split(' '), input='pybritivetest4.dev\n\n\n')
    common_asserts(result, substring='[tenant-pybritivetest4.dev]')


def test_configure_tenant_via_prompt_yes_alias(runner, cli):
    result = runner.invoke(cli, ['configure', 'tenant'], input='pybritivetest3.dev\ntestalias3\nyaml\n')
    common_asserts(result, substring='[tenant-testalias3]')


def test_configure_tenant_via_prompt_yes_alias_no_format(runner, cli):
    result = runner.invoke(cli, ['configure', 'tenant'], input='pybritivetest4.dev\ntestalias4\n\n')
    common_asserts(result, substring='[tenant-testalias4]')


def test_configure_global_via_flags_file_backend(runner, cli):
    result = runner.invoke(cli, 'configure global -t pybritivetest1.dev -f table -b file'.split(' '))
    common_asserts(
        result, substring=['default_tenant=pybritivetest1.dev', 'output_format=table', 'credential_backend=file']
    )


def test_configure_global_via_flags_encrypted_file_backend(runner, cli):
    result = runner.invoke(cli, 'configure global -t pybritivetest2.dev -f yaml -b encrypted-file'.split(' '))
    common_asserts(
        result,
        substring=['default_tenant=pybritivetest2.dev', 'output_format=yaml', 'credential_backend=encrypted-file'],
    )


def test_configure_global_via_prompt_file_backend(runner, cli):
    result = runner.invoke(cli, 'configure global'.split(' '), input='pybritivetest1.dev\ntable-pretty\nfile\n')
    common_asserts(
        result, substring=['default_tenant=pybritivetest1.dev', 'output_format=table-pretty', 'credential_backend=file']
    )


def test_configure_global_via_prompt_encrypted_file_backend(runner, cli):
    result = runner.invoke(cli, 'configure global'.split(' '), input='pybritivetest2.dev\n\nencrypted-file\n')
    common_asserts(
        result,
        substring=['default_tenant=pybritivetest2.dev', 'output_format=json', 'credential_backend=encrypted-file'],
    )


def test_configure_global_with_invalid_format(runner, cli):
    result = runner.invoke(cli, 'configure global -f error -P'.split(' '))
    assert "Invalid value for '--format' / '-f'" in result.output


def test_configure_global_with_invalid_tenant(runner, cli):
    result = runner.invoke(cli, 'configure global -t incorrect'.split(' '))
    assert 'Invalid global field default_tenant value incorrect provided. Tenant not found.' in result.output


def test_configure_update_global_invalid_data(runner, cli):
    result = runner.invoke(cli, 'configure update global default_tenant incorrect'.split(' '))
    assert result.exit_code == 1
    assert 'Invalid global field default_tenant value incorrect provided. Tenant not found.' in result.output


def test_configure_update_invalid_section(runner, cli):
    result = runner.invoke(cli, 'configure update test default_tenant incorrect'.split(' '))
    assert result.exit_code == 1
    assert 'Cannot save config file due to invalid data provided.' in result.output


def test_configure_update_tenant_correct_data(runner, cli):
    tenant = os.getenv('PYBRITIVE_TEST_TENANT')
    result = runner.invoke(cli, f'configure update tenant-{tenant} name {tenant}'.split(' '))
    common_asserts(result, substring=['name=pybritivetest1.dev'])


def test_configure_update_global_correct_data(runner, cli):
    tenant = os.getenv('PYBRITIVE_TEST_TENANT')
    result = runner.invoke(cli, f'configure update global default_tenant {tenant}')
    common_asserts(result, substring=[f'default_tenant={tenant}'])


def test_configure_update_aws_data(runner, cli):
    result = runner.invoke(cli, 'configure update aws default_checkout_mode integrate'.split(' '))
    common_asserts(result, substring=['aws', 'default_checkout_mode=integrate'])
