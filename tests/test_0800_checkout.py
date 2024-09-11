import json
import os

PROFILE = os.getenv('PYBRITIVE_TEST_PROFILE')


def test_checkout_json(runner, cli):
    result = runner.invoke(cli, ['checkout', PROFILE, '-m', 'json'])
    assert result.exit_code == 0
    creds = json.loads(result.output)
    assert 'AccessKeyId' in creds
    assert 'SecretAccessKey' in creds
    assert 'SessionToken' in creds
    assert 'Expiration' in creds


def test_checkout_aws_credential_process(runner, cli):
    result = runner.invoke(cli, ['checkout', PROFILE, '-m', 'awscredentialprocess'])
    assert result.exit_code == 0
    creds = json.loads(result.output)
    assert 'AccessKeyId' in creds
    assert 'SecretAccessKey' in creds
    assert 'SessionToken' in creds
    assert 'Expiration' in creds
    assert 'Version' in creds
