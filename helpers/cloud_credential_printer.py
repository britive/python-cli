import json
import click
import platform
import configparser
import os
from pathlib import Path


# trailing spaces matter as some options do not have the trailing space
env_options = {
    'nix': 'export ',
    'winps': '$Env:',
    'wincmd': 'set '
}


class CloudCredentialPrinter:
    def __init__(self, app_type, console, mode, profile, credentials):
        self.app_type = app_type
        self.profile = profile
        self.console = console
        helper = mode.split('-')
        env_prefix = helper[1] if 1 < len(helper) else None
        self.mode = helper[0]
        self.credentials = credentials
        self.on_windows = True if platform.system().lower() == 'windows' else False
        if env_prefix:
            self.env_command = env_options[env_prefix]
        else:
            self.env_command = env_options['wincmd'] if self.on_windows else env_options['nix']

    def print(self):
        mode_prefix = self.mode.split('-')[0]
        if mode_prefix == 'text':
            self.print_text()
        if mode_prefix == 'json':
            self.print_json()
        if mode_prefix == 'env':
            self.print_env()
        if mode_prefix == 'integrate':
            self.print_integrate()
        if mode_prefix == 'azlogin':
            self.print_azlogin()
        if mode_prefix == 'awscredentialprocess':
            self.print_awscredentialprocess()
        if mode_prefix == 'azps':
            self.print_azps()

    def print_text(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')

    def print_json(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')

    def print_env(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')

    def print_integrate(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')

    def print_awscredentialprocess(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')

    def print_azlogin(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')

    def print_azps(self):
        raise NotImplementedError(f'Application type {self.app_type} does not support the specified mode.')


class AwsCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, credentials):
        super().__init__('AWS', console, mode, profile, credentials)

    def print_text(self):
        click.echo('AWS_ACCESS_KEY_ID')
        click.echo(self.credentials['accessKeyID'])
        click.echo('')

        click.echo('AWS_SECRET_ACCESS_KEY')
        click.echo(self.credentials['secretAccessKey'])
        click.echo('')

        click.echo('AWS_SESSION_TOKEN')
        click.echo(self.credentials['sessionToken'])
        click.echo('')

        click.echo('AWS_EXPIRATION')
        click.echo(self.credentials['expirationTime'])
        click.echo('')

    def print_json(self, version=None):
        creds = {
            'AccessKeyId': self.credentials['accessKeyID'],
            'SecretAccessKey': self.credentials['secretAccessKey'],
            'SessionToken': self.credentials['sessionToken'],
            'Expiration': self.credentials['expirationTime']
        }
        if version:
            creds['Version'] = version
        click.echo(json.dumps(creds, indent=2))

    def print_env(self):
        click.echo(f'{self.env_command}AWS_ACCESS_KEY_ID="{self.credentials["accessKeyID"]}"')
        click.echo(f'{self.env_command}AWS_SECRET_ACCESS_KEY="{self.credentials["secretAccessKey"]}"')
        click.echo(f'{self.env_command}AWS_SESSION_TOKEN="{self.credentials["sessionToken"]}"')
        click.echo(f'{self.env_command}AWS_EXPIRATION="{self.credentials["expirationTime"]}"')

    def print_integrate(self):
        # get path to aws credentials file
        env_path = os.getenv('AWS_SHARED_CREDENTIALS_FILE')
        if not env_path:
            path = Path.home() / '.aws' / 'credentials'  # handle os specific separators properly
        else:
            path = Path(env_path)

        # if credentials file does not yet exist, create it as an empty file
        if not path.is_file():
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

        # open the file with configparser
        config = configparser.ConfigParser()
        config.read(str(path))

        # add the new profile/section
        config[self.profile] = {
            'aws_access_key_id': self.credentials["accessKeyID"],
            'aws_secret_access_key': self.credentials["secretAccessKey"],
            'aws_session_token': self.credentials["sessionToken"],
            'aws_expiration': self.credentials["expirationTime"]
        }

        # write the new credentials file
        with open(str(path), 'w') as f:
            config.write(f, space_around_delimiters=False)

    def print_awscredentialprocess(self):
        self.print_json(version=1)


class AzureCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, credentials):
        key = list(credentials.keys())[0]
        credentials = json.loads(credentials[key])
        super().__init__('Azure', console, mode, profile, credentials)

    def print_text(self):
        click.echo('TENANT')
        click.echo(self.credentials['tenantId'])
        click.echo('')

        click.echo('USERNAME/APP ID/CLIENT ID')
        click.echo(self.credentials['appId'])
        click.echo('')

        click.echo('PASSWORD/SECRET TEXT/CLIENT SECRET')
        click.echo(self.credentials['secretText'])
        click.echo('')

    def print_json(self, version=None):
        creds = {
            'TenantId': self.credentials['tenantId'],
            'ClientId': self.credentials['appId'],
            'ClientSecret': self.credentials['secretText']
        }
        if version:
            creds['Version'] = version
        click.echo(json.dumps(creds, indent=2))

    def print_env(self):
        click.echo(f'{self.env_command}AZURE_CLIENT_ID="{self.credentials["appId"]}"')
        click.echo(f'{self.env_command}AZURE_CLIENT_SECRET="{self.credentials["secretText"]}"')
        click.echo(f'{self.env_command}AZURE_TENANT_ID="{self.credentials["tenantId"]}"')

    def print_azlogin(self):
        click.echo(self.credentials['cliLogin'])

    def print_azps(self):
        click.echo(self.credentials['powershellScript'].replace('\n ', '\n'))
