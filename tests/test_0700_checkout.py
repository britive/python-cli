import json


def test_checkout_json(runner, cli, profile):
    result = runner.invoke(cli, ['checkout', profile, '-m', 'json'])
    assert result.exit_code == 0
    creds = json.loads(result.output)
    assert 'AccessKeyId' in creds.keys()
    assert 'SecretAccessKey' in creds.keys()
    assert 'SessionToken' in creds.keys()
    assert 'Expiration' in creds.keys()


def test_checkout_aws_credential_process(runner, cli, profile):
    result = runner.invoke(cli, ['checkout', profile, '-m', 'awscredentialprocess'])
    assert result.exit_code == 0
    creds = json.loads(result.output)
    assert 'AccessKeyId' in creds.keys()
    assert 'SecretAccessKey' in creds.keys()
    assert 'SessionToken' in creds.keys()
    assert 'Expiration' in creds.keys()
    assert 'Version' in creds.keys()
