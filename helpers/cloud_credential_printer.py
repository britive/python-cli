import json
import click
import platform


# trailing spaces matter as some options do not have the trailing space
env_options = {
    'nix': 'export ',
    'winps': '$Env:',
    'wincmd': 'set '
}


class CloudCredentialPrinter:
    def __init__(self, console, mode, credentials):
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

    def print_text(self):
        raise NotImplemented()

    def print_json(self):
        raise NotImplemented()

    def print_env(self):
        raise NotImplemented()

    def print_integrate(self):
        raise NotImplemented()

    def print_awscredentialprocess(self):
        raise NotImplemented()


class AwsCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, credentials):
        super().__init__(console, mode, credentials)

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
        pass

    def print_awscredentialprocess(self):
        self.print_json(version=1)

