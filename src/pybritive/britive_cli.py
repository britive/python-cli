import io
from britive.britive import Britive
from .helpers.config import ConfigManager
from .helpers.credentials import FileCredentialManager
import json
import click
import csv
from tabulate import tabulate
import yaml
from .helpers import cloud_credential_printer as printer
from britive import exceptions
from pathlib import Path


default_table_format = 'fancy_grid'


class BritiveCli:
    def __init__(self, tenant_name: str = None, token: str = None, silent: bool = False):
        self.silent = silent
        self.output_format = None
        self.tenant_name = None
        self.tenant_alias = None
        self.token = token
        self.b = None
        self.available_profiles = None
        self.config = ConfigManager(tenant_name=tenant_name, cli=self)
        self.list_separator = '|'

    def set_output_format(self, output_format: str):
        self.output_format = self.config.get_output_format(output_format)

    def login(self, explicit: bool = False):
        self.tenant_name = self.config.get_tenant()['name']
        self.tenant_alias = self.config.alias
        if explicit and self.token:
            raise click.ClickException('Interactive login unavailable when an API token is provided.')

        if self.token:
            try:
                self.b = Britive(
                    tenant=self.tenant_name,
                    token=self.token,
                    query_features=True
                )
            except exceptions.UnauthorizedRequest as e:
                raise click.ClickException('Invalid API token provided.')
        else:
            while True:  # will break after we successfully get logged in
                try:
                    self.b = Britive(
                        tenant=self.tenant_name,
                        token=FileCredentialManager(
                            tenant_alias=self.tenant_alias,
                            tenant_name=self.tenant_name,
                            cli=self
                        ).get_token(),
                        query_features=True
                    )
                    break
                except exceptions.UnauthorizedRequest as e:
                    self._cleanup_credentials()

    def _cleanup_credentials(self):
        FileCredentialManager(
            tenant_alias=self.tenant_alias,
            tenant_name=self.tenant_name,
            cli=self
        ).delete()

    def logout(self):
        if self.token:
            raise click.ClickException('Logout not available when using an API token.')
        self.login()
        self.b.delete(f'https://{self.tenant_name}.britive-app.com/api/auth')
        self._cleanup_credentials()

    # will take a list of dicts and print to the screen based on the format specified in the config file
    # dict can only be 1 level deep (no nesting) - caller needs to massage the data accordingly
    def print(self, data: object, ignore_silent: bool = False):
        if self.silent and not ignore_silent:
            return

        if isinstance(data, str):  # if we have a string just print it and move on
            click.echo(data)
            return

        if self.output_format == 'json':
            click.echo(json.dumps(data, indent=2, default=str))
        elif self.output_format == 'list':
            for row in data:
                click.echo(self.list_separator.join(row.values()))
        elif self.output_format == 'csv':
            fields = list(data[0].keys())
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fields, delimiter=',')
            writer.writeheader()
            writer.writerows(data)
            click.echo(output.getvalue())
        elif self.output_format.startswith('table'):
            if isinstance(data, dict):
                data = [data]
            tablefmt = default_table_format
            split = self.output_format.split('-')
            if len(split) > 1:
                tablefmt = split[1]
            click.echo(tabulate(data, headers='keys', tablefmt=tablefmt))
        elif self.output_format == 'yaml':
            y = yaml.safe_load(json.dumps(data))
            click.echo(yaml.safe_dump(y))
        else:
            raise click.ClickException(f'Invalid output format {self.output_format} provided.')

    def user(self):
        self.login()
        username = self.b.my_access.whoami()['user']['username']
        alias = self.tenant_alias
        output = f'{username} @ {self.tenant_name}'
        if alias != self.tenant_name:
            output += f' (alias: {alias})'
        self.print(output)

    def list_secrets(self):
        self.login()
        self.print(self.b.my_secrets.list())

    def list_profiles(self, checked_out: bool = False):
        self.login()
        data = []
        checked_out = [p['papId'] for p in self.b.my_access.list_checked_out_profiles()] if checked_out else []
        for app in self.b.my_access.list_profiles():
            for profile in app.get('profiles', []):
                for env in profile.get('environments', []):
                    if not checked_out or profile['profileId'] in checked_out:
                        row = {
                            'Application': app['appName'],
                            'Environment Name': env['environmentName'],
                            'Profile Name': profile['profileName'],
                            'Description': profile['profileDescription'],
                            'Type': app['catalogAppName']
                        }
                        if self.output_format == 'list':
                            self.list_separator = '/'
                            row.pop('Description')
                            row.pop('Type')
                        data.append(row)
        self.print(data)

    def list_applications(self):
        self.login()
        data = []
        for app in self.b.my_access.list_profiles():
            row = {
                'Application': app['appName'],
                'Type': app['catalogAppName'],
                'Description': app['appDescription'],

            }
            data.append(row)
        self.print(data)

    def list_environments(self):
        self.login()
        data = []
        for app in self.b.my_access.list_profiles():
            for profile in app.get('profiles', []):
                for env in profile.get('environments', []):
                    row = {
                        'Application': app['appName'],
                        'Environment': env['environmentName'],
                        'Description': env['environmentDescription'],
                        'Type': app['catalogAppName']
                    }
                    data.append(row)
        self.print(data)

    def _set_available_profiles(self):
        if not self.available_profiles:
            data = []
            for app in self.b.my_access.list_profiles():
                for profile in app.get('profiles', []):
                    for env in profile.get('environments', []):
                        row = {
                            'app_name': app['appName'],
                            'app_id': app['appContainerId'],
                            'app_type': app['catalogAppName'],
                            'env_name': env['environmentName'],
                            'env_id': env['environmentId'],
                            'profile_name': profile['profileName'],
                            'profile_id': profile['profileId'],
                            'profile_allows_console': profile['consoleAccess'],
                            'profile_allows_programmatic': profile['programmaticAccess']
                        }
                        data.append(row)
            self.available_profiles = data

    def _get_app_type(self, application_id):
        self._set_available_profiles()
        for profile in self.available_profiles:
            if profile['app_id'] == application_id:
                return profile['app_type']
        raise click.ClickException(f'Application {application_id} not found')

    def __get_cloud_credential_printer(self, app_type, console, mode, profile, silent, credentials):
        if app_type in ['AWS', 'AWS Standalone']:
            return printer.AwsCloudCredentialPrinter(
                console=console,
                mode=mode,
                profile=profile,
                credentials=credentials,
                silent=silent,
                cli=self
            )
        if app_type in ['Azure']:
            return printer.AzureCloudCredentialPrinter(
                console=console,
                mode=mode,
                profile=profile,
                credentials=credentials,
                silent=silent,
                cli=self
            )
        if app_type in ['GCP']:
            return printer.GcpCloudCredentialPrinter(
                console=console,
                mode=mode,
                profile=profile,
                credentials=credentials,
                silent=silent,
                cli=self
            )

    def checkin(self, profile):
        self.login()
        profile = self.config.profile_aliases.get(profile, profile)
        parts = profile.split('/')
        if len(parts) != 3:
            raise click.ClickException('Provided profile string does not have the required 3 parts.')
        app_name = parts[0]
        env_name = parts[1]
        profile_name = parts[2]

        self.b.my_access.checkin_by_name(
            profile_name=profile_name,
            environment_name=env_name,
            application_name=app_name
        )

    def checkout(self, alias, blocktime, console, justification, mode, maxpolltime, profile):
        self.login()
        # first check if this is a profile alias
        profile_or_alias = alias or profile
        profile = self.config.profile_aliases.get(profile, profile)
        parts = profile.split('/')
        if len(parts) != 3:
            raise click.ClickException('Provided profile string does not have the required 3 parts.')
        app_name = parts[0]
        env_name = parts[1]
        profile_name = parts[2]

        try:
            response = self.b.my_access.checkout_by_name(
                profile_name=profile_name,
                environment_name=env_name,
                application_name=app_name,
                programmatic=False if console else True,
                include_credentials=True,
                wait_time=blocktime,
                max_wait_time=maxpolltime,
                justification=justification
            )
        except exceptions.ApprovalRequiredButNoJustificationProvided:
            raise click.ClickException('approval required and no justification provided.')
        except ValueError as e:
            raise click.BadParameter(str(e))

        if alias:  # do this down here so we know that the profile is valid and a checkout was successful
            self.config.save_profile_alias(alias=alias, profile=profile)

        app_container_id = response['appContainerId']
        app_type = self._get_app_type(app_container_id)
        cc_printer = self.__get_cloud_credential_printer(
            app_type,
            console,
            mode,
            profile_or_alias,
            self.silent,
            response['credentials']
        )
        cc_printer.print()

    def import_existing_npm_config(self):
        profile_aliases = self.config.import_global_npm_config()
        if len(profile_aliases.keys()) == 0:
            return
        self.print('')
        self.print('Profile aliases exist...will retrieve profile details from the tenant.')
        self.print('')

        self.login()
        self._set_available_profiles()
        self.print('')

        for alias, ids in profile_aliases.items():
            if '/' in alias:
                continue
            app, env, profile, cloud = ids.split('/')
            for p in self.available_profiles:
                if p['app_id'] == app and p['env_id'] == env and p['profile_id'] == profile:
                    profile_str = f"{p['app_name']}/{p['env_name']}/{p['profile_name']}"
                    self.config.save_profile_alias(alias, profile_str)
                    self.print(f'Saved alias {alias} to profile {profile_str}')

    def configure_tenant(self, tenant, alias, output_format):
        self.config.save_tenant(
            tenant=tenant,
            alias=alias,
            output_format=output_format
        )

    def configure_global(self, default_tenant_name, output_format):
        self.config.save_global(
            default_tenant_name=default_tenant_name,
            output_format=output_format
        )

    def viewsecret(self, path, blocktime, justification,maxpolltime):
        self.login()

        try:
            value = self.b.my_secrets.view(
                path=path,
                justification=justification,
                wait_time=blocktime,
                max_wait_time=maxpolltime
            )
        except exceptions.AccessDenied:
            raise click.ClickException('user does not have access to the secret.')
        except exceptions.ApprovalRequiredButNoJustificationProvided:
            raise click.ClickException('approval required and no justification provided.')

        # handle the generic note template type for a better UX
        if len(value.keys()) == 1 and 'Note' in value.keys():
            value = value['Note']

        # if the value can be converted from JSON to python dict, do it
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
        except TypeError:
            pass

        # and finally print the secret data
        self.print(value)

    def downloadsecret(self, path, blocktime, justification,maxpolltime, file):
        self.login()

        try:
            response = self.b.my_secrets.download(
                path=path,
                justification=justification,
                wait_time=blocktime,
                max_wait_time=maxpolltime
            )
        except exceptions.AccessDenied:
            raise click.ClickException('user does not have access to the secret.')
        except exceptions.ApprovalRequiredButNoJustificationProvided:
            raise click.ClickException('approval required and no justification provided.')

        filename_from_secret = response['filename']
        content = response['content_bytes']

        if file == '-':
            try:
                self.print(content.decode('utf-8'))
            except UnicodeDecodeError as e:
                raise click.ClickException(
                    'Secret file contents cannot be decoded to utf-8. '
                    'Save the contents of the file to disk instead.'
                )
            return

        filename = file or filename_from_secret
        path = str(Path(filename).absolute())
        with open(path, 'wb') as f:
            f.write(content)
        self.print(f'wrote contents of secret file to {path}')








