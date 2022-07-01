import io
from britive.britive import Britive
from config import ConfigManager
from credentials import FileCredentialManager
import json
import typer
import csv
from tabulate import tabulate
import yaml


default_table_format = 'fancy_grid'


class BritiveCli:
    def __init__(self, tenant_name: str = None, token: str = None):
        self.config = ConfigManager(tenant_name=tenant_name)
        self.output_format = None
        self.tenant_name = self.config.selected_tenant['name']
        self.tenant_alias = self.config.alias
        self.token = token
        self.b = None

    def set_output_format(self, output_format: str):
        self.output_format = self.config.get_output_format(output_format)

    def login(self, explicit: bool = False):
        if explicit and self.token:
            typer.echo('Interactive login unavailable when an API token is provided.')
            typer.Abort()
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
            typer.echo(data)
            return

        if isinstance(data, dict):
            data = [data]

        if self.output_format == 'json':
            typer.echo(json.dumps(data, indent=2, default=str))
        elif self.output_format == 'csv':
            fields = list(data[0].keys())
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=fields, delimiter=',')
            writer.writeheader()
            writer.writerows(data)
            typer.echo(output.getvalue())
        elif self.output_format.startswith('table'):
            tablefmt = default_table_format
            split = self.output_format.split('-')
            if len(split) > 1:
                tablefmt = split[1]
            typer.echo(tabulate(data, headers='keys', tablefmt=tablefmt))
        elif self.output_format == 'yaml':
            y = yaml.safe_load(json.dumps(data))
            typer.secho(yaml.safe_dump(y))
        else:
            typer.echo(f'Invalid output format {self.output_format} provided.')
            typer.Abort()

    def user(self):
        self.login()
        self.print(self.b.my_access.whoami()['user']['username'])

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
