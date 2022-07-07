import io
from britive.britive import Britive
from helpers.config import ConfigManager
from helpers.credentials import FileCredentialManager
import json
import click
import csv
from tabulate import tabulate
import yaml
import helpers.cloud_credential_printer as printer


default_table_format = 'fancy_grid'


class BritiveCli:
    def __init__(self, tenant_name: str = None, token: str = None):
        self.config = ConfigManager(tenant_name=tenant_name)
        self.output_format = None
        self.tenant_name = self.config.selected_tenant['name']
        self.tenant_alias = self.config.alias
        self.token = token
        self.b = None
        self.available_profiles = None

    def set_output_format(self, output_format: str):
        self.output_format = self.config.get_output_format(output_format)

    def login(self, explicit: bool = False):
        if explicit and self.token:
            click.echo('Interactive login unavailable when an API token is provided.')
            exit()
        self.b = Britive(
            tenant=self.tenant_name,
            token=self.token or FileCredentialManager(
                tenant_alias=self.tenant_alias,
                tenant_name=self.tenant_name
            ).get_token(),
            query_features=False
        )

    def logout(self):
        FileCredentialManager(tenant_alias=self.tenant_alias, tenant_name=self.tenant_name).delete()

    # will take a list of dicts and print to the screen based on the format specified in the config file
    # dict can only be 1 level deep (no nesting) - caller needs to massage the data accordingly
    def print(self, data: object):
        if isinstance(data, str):  # if we have a string just print it and move on
            click.echo(data)
            return

        if isinstance(data, dict):
            data = [data]

        if self.output_format == 'json':
            click.echo(json.dumps(data, indent=2, default=str))
        elif self.output_format == 'csv':
            fields = list(data[0].keys())
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fields, delimiter=',')
            writer.writeheader()
            writer.writerows(data)
            click.echo(output.getvalue())
        elif self.output_format.startswith('table'):
            tablefmt = default_table_format
            split = self.output_format.split('-')
            if len(split) > 1:
                tablefmt = split[1]
            click.echo(tabulate(data, headers='keys', tablefmt=tablefmt))
        elif self.output_format == 'yaml':
            y = yaml.safe_load(json.dumps(data))
            click.secho(yaml.safe_dump(y))
        else:
            click.echo(f'Invalid output format {self.output_format} provided.')
            exit()

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

    def list_profiles(self):
        self.login()
        data = []
        for app in self.b.my_access.list_profiles():
            for profile in app.get('profiles', []):
                for env in profile.get('environments', []):
                    row = {
                        'Application': app['appName'],
                        'Environment Name': env['environmentName'],
                        'Profile Name': profile['profileName'],
                        'Description': profile['profileDescription'],
                        'Type': app['catalogAppName']
                    }
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
        click.echo('application not found')
        exit()

    @staticmethod
    def __get_cloud_credential_printer(app_type, console, mode, profile, credentials):
        if app_type in ['AWS', 'AWS Standalone']:
            return printer.AwsCloudCredentialPrinter(
                console=console,
                mode=mode,
                profile=profile,
                credentials=credentials
            )
        if app_type in ['Azure']:
            return printer.AzureCloudCredentialPrinter(
                console=console,
                mode=mode,
                profile=profile,
                credentials=credentials
            )

    def checkin(self, profile):
        self.login()
        profile = self.config.profile_aliases.get(profile, profile)
        parts = profile.split('/')
        if len(parts) != 3:
            click.echo('Provided profile string does not have the required 3 parts.')
            exit()
        app_name = parts[0]
        env_name = parts[1]
        profile_name = parts[2]

        self.b.my_access.checkin_by_name(
            profile_name=profile_name,
            environment_name=env_name,
            application_name=app_name
        )

    def checkout(self, alias, blocktime, console, justification, mode, maxpolltime, silent, profile):
        self.login()
        # first check if this is a profile alias
        profile_or_alias = alias or profile
        profile = self.config.profile_aliases.get(profile, profile)
        parts = profile.split('/')
        if len(parts) != 3:
            click.echo('Provided profile string does not have the required 3 parts.')
            exit()
        app_name = parts[0]
        env_name = parts[1]
        profile_name = parts[2]

        response = self.b.my_access.checkout_by_name(
            profile_name=profile_name,
            environment_name=env_name,
            application_name=app_name,
            programmatic=False if console else True,
            include_credentials=True
        )

        if alias:  # do this down here so we know that the profile is valid and a checkout was successful
            self.config.save_profile_alias(alias=alias, profile=profile)

        app_container_id = response['appContainerId']
        app_type = self._get_app_type(app_container_id)
        cc_printer = self.__get_cloud_credential_printer(
            app_type,
            console,
            mode,
            profile_or_alias,
            response['credentials']
        )
        cc_printer.print()




