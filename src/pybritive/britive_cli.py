import io
import time

from britive.britive import Britive
from .helpers.config import ConfigManager
from .helpers.credentials import FileCredentialManager, EncryptedFileCredentialManager
import json
import click
import csv
from tabulate import tabulate
import yaml
from .helpers import cloud_credential_printer as printer
from .helpers.cache import Cache
from britive import exceptions
from pathlib import Path
from datetime import datetime


default_table_format = 'fancy_grid'


class BritiveCli:
    def __init__(self, tenant_name: str = None, token: str = None, silent: bool = False, passphrase: str = None):
        self.silent = silent
        self.output_format = None
        self.tenant_name = None
        self.tenant_alias = None
        self.token = token
        self.b = None
        self.available_profiles = None
        self.config = ConfigManager(tenant_name=tenant_name, cli=self)
        self.list_separator = '|'
        self.passphrase = passphrase
        self.credential_manager = None

    def set_output_format(self, output_format: str):
        self.output_format = self.config.get_output_format(output_format)

    def set_credential_manager(self):
        if self.credential_manager:
            return
        backend = self.config.backend()
        if backend == 'file':
            self.credential_manager = FileCredentialManager(
                tenant_alias=self.tenant_alias,
                tenant_name=self.tenant_name,
                cli=self
            )
        elif backend == 'encrypted-file':
            self.credential_manager = EncryptedFileCredentialManager(
                tenant_alias=self.tenant_alias,
                tenant_name=self.tenant_name,
                cli=self,
                passphrase=self.passphrase
            )
        else:
            raise click.ClickException(f'invalid credential backend {backend}.')

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
                    query_features=False
                )
            except exceptions.UnauthorizedRequest:
                raise click.ClickException('Invalid API token provided.')
        else:
            while True:  # will break after we successfully get logged in
                try:
                    self.set_credential_manager()
                    self.b = Britive(
                        tenant=self.tenant_name,
                        token=self.credential_manager.get_token(),
                        query_features=False
                    )
                    break
                except exceptions.UnauthorizedRequest as e:
                    self._cleanup_credentials()

        # if user called `pybritive login` and we should refresh the profile cache...do so
        if explicit and self.config.auto_refresh_profile_cache():
            self._set_available_profiles()
            self.cache_profiles()

    def _cleanup_credentials(self):
        self.set_credential_manager()
        self.credential_manager.delete()

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
        self._set_available_profiles()
        data = []
        checked_out_profiles = [p['papId'] for p in self.b.my_access.list_checked_out_profiles()] if checked_out else []

        for profile in self.available_profiles:
            if not checked_out or profile['profile_id'] in checked_out_profiles:
                row = {
                    'Application': profile['app_name'],
                    'Environment': profile['env_name'],
                    'Profile': profile['profile_name'],
                    'Description': profile['profile_description'],
                    'Type': profile['app_type']
                }
                if self.output_format == 'list':
                    self.list_separator = '/'
                    row.pop('Description')
                    row.pop('Type')
                data.append(row)
        self.print(data)

    def list_applications(self):
        self.login()
        self._set_available_profiles()
        keys = ['app_name', 'app_type', 'app_description']
        apps = []
        for profile in self.available_profiles:
            apps.append({k: v for k, v in profile.items() if k in keys})
        apps = [dict(t) for t in {tuple(d.items()) for d in apps}]  # de-dup
        data = []
        for app in apps:
            row = {
                'Application': app['app_name'],
                'Type': app['app_type'],
                'Description': app['app_description'],

            }
            data.append(row)
        self.print(data)

    def list_environments(self):
        self.login()
        self._set_available_profiles()
        envs = []
        keys = ['app_name', 'app_type', 'env_name', 'env_description']
        for profile in self.available_profiles:
            envs.append({k: v for k, v in profile.items() if k in keys})
        envs = [dict(t) for t in {tuple(d.items()) for d in envs}]  # de-dup

        data = []
        for env in envs:
            row = {
                'Application': env['app_name'],
                'Environment': env['env_name'],
                'Description': env['env_description'],
                'Type': env['app_type']
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
                            'app_description': app['appDescription'],
                            'env_name': env['environmentName'],
                            'env_id': env['environmentId'],
                            'env_description': env['environmentDescription'],
                            'profile_name': profile['profileName'],
                            'profile_id': profile['profileId'],
                            'profile_allows_console': profile['consoleAccess'],
                            'profile_allows_programmatic': profile['programmaticAccess'],
                            'profile_description': profile['profileDescription']
                        }
                        data.append(row)
            self.available_profiles = data
        if self.config.auto_refresh_profile_cache():
            self.cache_profiles(load=False)

    def _get_app_type(self, application_id):
        self._set_available_profiles()
        for profile in self.available_profiles:
            if profile['app_id'] == application_id:
                return profile['app_type']
        raise click.ClickException(f'Application {application_id} not found')

    def __get_cloud_credential_printer(self, app_type, console, mode, profile, silent, credentials,
                                       aws_credentials_file):
        if app_type in ['AWS', 'AWS Standalone']:
            return printer.AwsCloudCredentialPrinter(
                console=console,
                mode=mode,
                profile=profile,
                credentials=credentials,
                silent=silent,
                cli=self,
                aws_credentials_file=aws_credentials_file
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
        parts = self._split_profile_into_parts(profile)

        self.b.my_access.checkin_by_name(
            profile_name=parts['profile'],
            environment_name=parts['env'],
            application_name=parts['app']
        )

    def _checkout(self, profile_name, env_name, app_name, programmatic, blocktime, maxpolltime, justification):
        try:
            self.login()
            return self.b.my_access.checkout_by_name(
                profile_name=profile_name,
                environment_name=env_name,
                application_name=app_name,
                programmatic=programmatic,
                include_credentials=True,
                wait_time=blocktime,
                max_wait_time=maxpolltime,
                justification=justification
            )
        except exceptions.ApprovalRequiredButNoJustificationProvided:
            raise click.ClickException('approval required and no justification provided.')
        except ValueError as e:
            raise click.BadParameter(str(e))

    @staticmethod
    def _should_check_force_renew(app, force_renew, console):
        return app in ['AWS', 'AWS Standalone'] and force_renew and not console


    def _split_profile_into_parts(self, profile):
        profile_real = self.config.profile_aliases.get(profile, profile)
        parts = profile_real.split('/')
        if len(parts) != 3:
            raise click.ClickException('Provided profile string does not have the required 3 parts.')
        parts_dict = {
            'app': parts[0],
            'env': parts[1],
            'profile': parts[2]
        }
        return parts_dict

    def checkout(self, alias, blocktime, console, justification, mode, maxpolltime, profile, passphrase,
                 force_renew, aws_credentials_file):
        credentials = None
        app_type = None
        credential_process_creds_found = False
        response = None

        if mode == 'awscredentialprocess':
            self.silent = True  # the aws credential process CANNOT output anything other than the expected JSON
            # we need to check the credential process cache for the credentials first
            # then check to see if they are expired
            # if not simply return those credentials
            # if they are expired
            app_type = 'AWS'  # just hardcode as we know for sure this is for AWS
            credentials = Cache(passphrase=passphrase).get_awscredentialprocess(profile_name=alias or profile)
            if credentials:
                expiration_timestamp_str = credentials['expirationTime'].replace('Z', '')
                expires = datetime.fromisoformat(expiration_timestamp_str)
                now = datetime.utcnow()
                if now >= expires:  # check to ensure the credentials are still valid, if not, set to None and get new
                    credentials = None
                else:
                    credential_process_creds_found = True

        parts = self._split_profile_into_parts(profile)

        # create this params once so we can use it multiple places
        params = {
            'profile_name': parts['profile'],
            'env_name': parts['env'],
            'app_name': parts['app'],
            'programmatic': False if console else True,
            'blocktime': blocktime,
            'maxpolltime': maxpolltime,
            'justification': justification
        }

        if not credential_process_creds_found:  # nothing found via aws cred process or not aws cred process mode
            response = self._checkout(**params)
            app_type = self._get_app_type(response['appContainerId'])
            credentials = response['credentials']

        # this handles the --force-renew flag
        # lets check to see if the we should checkin this profile first and check it out again
        if self._should_check_force_renew(app_type, force_renew, console):
            expiration = datetime.fromisoformat(credentials['expirationTime'].replace('Z', ''))
            now = datetime.utcnow()
            diff = (expiration - now).total_seconds() / 60.0
            if diff < force_renew:  # time to checkin the profile so we can refresh creds
                self.print('checking in the profile to get renewed credentials....standby')
                self.checkin(profile=profile_real)
                response = self._checkout(**params)
                credential_process_creds_found = False  # need to write new creds to cache
                credentials = response['credentials']

        if alias:  # do this down here so we know that the profile is valid and a checkout was successful
            self.config.save_profile_alias(alias=alias, profile=profile)

        if mode == 'awscredentialprocess' and not credential_process_creds_found:
            Cache(passphrase=passphrase).save_awscredentialprocess(
                profile_name=alias or profile,
                credentials=credentials
            )

        self.__get_cloud_credential_printer(
            app_type,
            console,
            mode,
            alias or profile,
            self.silent,
            credentials,
            aws_credentials_file
        ).print()

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
            if '/' in alias:  # no need to import the aliases that aren't really aliases
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

    def configure_global(self, default_tenant_name, output_format, backend):
        self.config.save_global(
            default_tenant_name=default_tenant_name,
            output_format=output_format,
            backend=backend
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

    def cache_profiles(self, load=True):
        if load:
            self.login()
            self._set_available_profiles()
        profiles = []
        for p in self.available_profiles:
            profiles.append(f"{p['app_name']}/{p['env_name']}/{p['profile_name']}")
        Cache().save_profiles(profiles)

    @staticmethod
    def cache_clear():
        Cache().clear()

    def configure_update(self, section, field, value):
        self.config.update(section=section, field=field, value=value)

    def request_submit(self, profile, justification):
        self.login()
        parts = self._split_profile_into_parts(profile)

        self.b.my_access.request_approval_by_name(
            profile_name=parts['profile'],
            environment_name=parts['env'],
            application_name=parts['app'],
            block_until_disposition=False,
            justification=justification
        )

    def request_withdraw(self, profile):
        self.login()
        parts = self._split_profile_into_parts(profile)

        self.b.my_access.withdraw_approval_request_by_name(
            profile_name=parts['profile'],
            environment_name=parts['env'],
            application_name=parts['app']
        )











