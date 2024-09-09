import json


def test_checkout_json(runner, cli, profile):
    result = runner.invoke(cli, ['checkout', profile, '-m', 'json'])
    assert result.exit_code == 0
    creds = json.loads(result.output)
    assert 'AccessKeyId' in creds
    assert 'SecretAccessKey' in creds
    assert 'SessionToken' in creds
    assert 'Expiration' in creds


def test_checkout_aws_credential_process(runner, cli, profile):
    result = runner.invoke(cli, ['checkout', profile, '-m', 'awscredentialprocess'])
    assert result.exit_code == 0
    creds = json.loads(result.output)
    assert 'AccessKeyId' in creds
    assert 'SecretAccessKey' in creds
    assert 'SessionToken' in creds
    assert 'Expiration' in creds
    assert 'Version' in creds
