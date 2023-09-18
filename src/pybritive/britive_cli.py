import csv
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import io
import json
import os
import pathlib
from pathlib import Path
import sys
import uuid
import yaml

import click
import jmespath
from britive.britive import Britive
from britive import exceptions
from tabulate import tabulate
from .helpers.config import ConfigManager
from .helpers.credentials import FileCredentialManager, EncryptedFileCredentialManager
from .helpers.split import profile_split
from .helpers import cloud_credential_printer as printer
from .helpers.cache import Cache


default_table_format = 'fancy_grid'
debug_enabled = os.getenv('PYBRITIVE_DEBUG')


class BritiveCli:
    def __init__(self, tenant_name: str = None, token: str = None, silent: bool = False,
                 passphrase: str = None, federation_provider: str = None):
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
        self.federation_provider = federation_provider
        self.credential_manager = None
        self.verbose_checkout = False
        self.checkout_progress_previous_message = None
        self.browser = None

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
                cli=self,
                federation_provider=self.federation_provider,
                browser=self.browser
            )
        elif backend == 'encrypted-file':
            self.credential_manager = EncryptedFileCredentialManager(
                tenant_alias=self.tenant_alias,
                tenant_name=self.tenant_name,
                cli=self,
                passphrase=self.passphrase,
                federation_provider=self.federation_provider,
                browser=self.browser
            )
        else:
            raise click.ClickException(f'invalid credential backend {backend}.')

    def login(self, explicit: bool = False, browser: str = None):
        self.browser = browser
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
            except exceptions.UnauthorizedRequest as e:
                raise click.ClickException('Invalid API token provided.') from e
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
                except exceptions.UnauthorizedRequest:
                    self._cleanup_credentials()

        # if user called `pybritive login` and we should refresh the profile cache...do so
        if explicit and self.config.auto_refresh_profile_cache():
            self._set_available_profiles()
            self.cache_profiles()

    def _cleanup_credentials(self):
        self.set_credential_manager()
        self.credential_manager.delete()

    def logout(self):
        # if dealing with a token there is no concept of logout
        if self.token:
            raise click.ClickException('Logout not available when using an API token.')

        self.tenant_name = self.config.get_tenant()['name']
        self.tenant_alias = self.config.alias
        self.set_credential_manager()

        # let's see if we have credentials for this tenant already
        # if we do we need to invalidate them at the tenant and clean them up on the client side
        # if we don't have valid credentials for the tenant then there is no need to logout
        if self.credential_manager.has_valid_credentials():

            self.b = Britive(
                tenant=self.tenant_name,
                token=self.credential_manager.get_token(),
                query_features=False
            )
            self.b.delete(f'https://{Britive.parse_tenant(self.tenant_name)}/api/auth')
            self._cleanup_credentials()

    def debug(self, data: object, ignore_silent: bool = False):
        if debug_enabled:
            self.print(data=data, ignore_silent=ignore_silent)

    # will be passed to the britive checkout_by_name progress_func parameter when appropriate
    def checkout_callback_printer(self, message: str):
        if self.silent or not sys.stdout.isatty():
            return
        if message == 'complete':
            click.echo('')
            return

        if self.verbose_checkout:
            if self.checkout_progress_previous_message != message:
                newline = '\n' if self.checkout_progress_previous_message else ''
                self.checkout_progress_previous_message = message
                click.echo(f'{newline}{message} ', nl=False)
            else:
                click.echo('.', nl=False)
        else:
            click.echo('.', nl=False)

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
        elif self.output_format == 'list-profiles':
            for row in data:
                click.echo(self.list_separator.join([self.escape_profile_element(x) for x in row.values()]))
        elif self.output_format == 'list':
            for row in data:
                if isinstance(row, dict):
                    click.echo(self.list_separator.join([json.dumps(x, default=str) for x in row.values()]))
                elif isinstance(row, list):
                    click.echo(self.list_separator.join([json.dumps(x, default=str) for x in row]))
                else:
                    click.echo(row)
        elif self.output_format == 'csv':
            fields = list(data[0])
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
        username = self.b.my_access.whoami()['username']
        alias = self.tenant_alias
        output = f'{username} @ {self.tenant_name}'
        if alias != self.tenant_name:
            output += f' (alias: {alias})'
        self.print(output, ignore_silent=True)

    def list_secrets(self):
        self.login()
        self.print(self.b.my_secrets.list(), ignore_silent=True)

    def list_approvals(self):
        self.login()
        approvals = []
        for approval in self.b.my_access.list_approvals():
            approval.pop('resource', None)
            approval.pop('consumer', None)
            approval.pop('timeToApprove', None)
            approval.pop('validFor', None)
            approval.pop('action', None)
            approval.pop('approvers', None)
            approval.pop('expirationTimeApproval', None)
            approval.pop('updatedAt', None)
            approval.pop('actionBy', None)
            approval.pop('validForInDays', None)
            approvals.append(approval)

        approvals = sorted(approvals, key=lambda x: x['createdAt'])
        approvals.reverse()
        self.print(approvals, ignore_silent=True)

    def list_profiles(self, checked_out: bool = False):
        self.login()
        self._set_available_profiles()
        data = []
        checked_out_profiles = [
            f'{p["papId"]}-{p["environmentId"]}'
            for p in self.b.my_access.list_checked_out_profiles()
        ] if checked_out else []

        for profile in self.available_profiles:
            if not checked_out or f'{profile["profile_id"]}-{profile["env_id"]}' in checked_out_profiles:
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
                    if profile['2_part_profile_format_allowed']:
                        row.pop('Environment')
                data.append(row)

        # set special list output if needed
        if self.output_format == 'list':
            self.output_format = 'list-profiles'

        self.print(data, ignore_silent=True)

        # and set it back
        if self.output_format == 'list-profiles':
            self.output_format = 'list'

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
        self.print(data, ignore_silent=True)

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
        self.print(data, ignore_silent=True)

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
                            'env_short_name':  env['alternateEnvironmentName'],
                            'env_description': env['environmentDescription'],
                            'profile_name': profile['profileName'],
                            'profile_id': profile['profileId'],
                            'profile_allows_console': profile['consoleAccess'],
                            'profile_allows_programmatic': profile['programmaticAccess'],
                            'profile_description': profile['profileDescription'],
                            '2_part_profile_format_allowed': app['requiresHierarchicalModel']
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
                                       aws_credentials_file, gcloud_key_file):
        if app_type in ['AWS', 'AWS Standalone']:
            return printer.AwsCloudCredentialPrinter(
                console=console,
                mode=mode or self.config.aws_default_checkout_mode(),  # handle the aws default_checkout_mode here
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
                cli=self,
                gcloud_key_file=gcloud_key_file
            )
        return printer.GenericCloudCredentialPrinter(
            console=console,
            mode=mode,
            profile=profile,
            credentials=credentials,
            silent=silent,
            cli=self
        )

    def checkin(self, profile, console):
        self.login()
        self._set_available_profiles()
        parts = self._split_profile_into_parts(profile)

        ids = self._convert_names_to_ids(
            profile_name=parts['profile'],
            environment_name=parts['env'],
            application_name=parts['app']
        )

        access_type = 'CONSOLE' if console else 'PROGRAMMATIC'

        transaction_id = None
        application_type = None
        for checked_out_profile in self.b.my_access.list_checked_out_profiles():
            same_env = checked_out_profile['environmentId'] == ids['environment_id']
            same_profile = checked_out_profile['papId'] == ids['profile_id']
            same_access_type = checked_out_profile['accessType'] == access_type
            if all([same_env, same_profile, same_access_type]):
                transaction_id = checked_out_profile['transactionId']

                for available_profile in self.available_profiles:
                    same_env_2 = checked_out_profile['environmentId'] == available_profile['env_id']
                    same_profile_2 = checked_out_profile['papId'] == available_profile['profile_id']
                    if all([same_env_2, same_profile_2, access_type == 'PROGRAMMATIC']):
                        application_type = available_profile['app_type'].lower()
                        break
                break
        if not transaction_id:
            raise ValueError('no checked out profile found for the given profile')

        self.b.my_access.checkin(
            transaction_id=transaction_id
        )

        if application_type in ('aws', 'aws standalone'):
            self.clear_cached_aws_credentials(profile)

    def _checkout(self, profile_name, env_name, app_name, programmatic, blocktime, maxpolltime, justification):
        try:
            self.login()

            ids = self._convert_names_to_ids(
                profile_name=profile_name,
                environment_name=env_name,
                application_name=app_name
            )

            return self.b.my_access.checkout(
                profile_id=ids['profile_id'],
                environment_id=ids['environment_id'],
                programmatic=programmatic,
                include_credentials=True,
                wait_time=blocktime,
                max_wait_time=maxpolltime,
                justification=justification,
                progress_func=self.checkout_callback_printer  # callback will handle silent, isatty, etc.
            )
        except exceptions.ApprovalRequiredButNoJustificationProvided as e:
            raise click.ClickException('approval required and no justification provided.') from e
        except ValueError as e:
            raise click.BadParameter(str(e))
        except Exception as e:
            if 'programmatic access is not enabled' in str(e).lower():
                # attempt to automatically checkout console access instead
                # this is a cli only feature - not available in the sdk
                self.print('no programmatic access available - checking out console access instead')
                return self._checkout(profile_name, env_name, app_name, False, blocktime, maxpolltime, justification)
            raise e

    @staticmethod
    def _should_check_force_renew(app, force_renew, console):
        return app in ['AWS', 'AWS Standalone'] and force_renew and not console

    def _split_profile_into_parts(self, profile):
        profile_real = self.config.profile_aliases.get(profile.lower(), profile)
        parts = profile_split(profile_real)
        if len(parts) == 2:  # handle shortcut for profiles where the app and environment name are the same
            parts = [parts[0], parts[0], parts[1]]
        if len(parts) != 3:
            raise click.ClickException('Provided profile string does not have the required parts.')
        parts_dict = {
            'app': parts[0],
            'env': parts[1],
            'profile': parts[2]
        }
        return parts_dict

    def checkout(self, alias, blocktime, console, justification, mode, maxpolltime, profile, passphrase,
                 force_renew, aws_credentials_file, gcloud_key_file, verbose):
        credentials = None
        app_type = None
        credential_process_creds_found = False
        self.verbose_checkout = verbose

        # these 2 modes implicitly say that console access should be checked out without having to provide
        # the --console flag
        if mode and (mode == 'console' or mode.startswith('browser')):
            console = True
            if mode.startswith('browser'):
                self.browser = mode.replace('browser-', '')
            else:
                self.browser = os.getenv('PYBRITIVE_BROWSER')

        self._validate_justification(justification)

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
            'programmatic': not console,
            'blocktime': blocktime,
            'maxpolltime': maxpolltime,
            'justification': justification
        }

        if not credential_process_creds_found:  # nothing found via aws cred process or not aws cred process mode
            response = self._checkout(**params)
            app_type = self._get_app_type(response['appContainerId'])
            credentials = response['credentials']

        # this handles the --force-renew flag
        # lets check to see if we should checkin this profile first and check it out again
        if self._should_check_force_renew(app_type, force_renew, console):
            expiration = datetime.fromisoformat(credentials['expirationTime'].replace('Z', ''))
            now = datetime.utcnow()
            diff = (expiration - now).total_seconds() / 60.0
            if diff < force_renew:  # time to checkin the profile so we can refresh creds
                self.print('checking in the profile to get renewed credentials....standby')
                self.checkin(profile=profile)
                response = self._checkout(**params)
                credential_process_creds_found = False  # need to write new creds to cache
                credentials = response['credentials']

        if alias:  # do this down here, so we know that the profile is valid and a checkout was successful
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
            aws_credentials_file,
            gcloud_key_file
        ).print()

    def import_existing_npm_config(self):
        profile_aliases = self.config.import_global_npm_config()

        if len(profile_aliases) == 0:
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
            app, env, profile = ids.split('/')[:3]
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

    def viewsecret(self, path, blocktime, justification, maxpolltime):
        self._validate_justification(justification)
        self.login()

        try:
            value = self.b.my_secrets.view(
                path=path,
                justification=justification,
                wait_time=blocktime,
                max_wait_time=maxpolltime
            )
        except exceptions.AccessDenied as e:
            raise click.ClickException('user does not have access to the secret.') from e
        except exceptions.ApprovalRequiredButNoJustificationProvided as e:
            raise click.ClickException('approval required and no justification provided.') from e

        # handle the generic note template type for a better UX
        if len(value) == 1 and 'Note' in value:
            value = value['Note']

        # if the value can be converted from JSON to python dict, do it
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
        except TypeError:
            pass

        # and finally print the secret data
        self.print(value, ignore_silent=True)

    def downloadsecret(self, path, blocktime, justification, maxpolltime, file):
        self._validate_justification(justification)
        self.login()

        try:
            response = self.b.my_secrets.download(
                path=path,
                justification=justification,
                wait_time=blocktime,
                max_wait_time=maxpolltime
            )
        except exceptions.AccessDenied as e:
            raise click.ClickException('user does not have access to the secret.') from e
        except exceptions.ApprovalRequiredButNoJustificationProvided as e:
            raise click.ClickException('approval required and no justification provided.') from e

        filename_from_secret = response['filename']
        content = response['content_bytes']

        if file == '-':
            try:
                self.print(content.decode('utf-8'), ignore_silent=True)
            except UnicodeDecodeError as e:
                raise click.ClickException(
                    'Secret file contents cannot be decoded to utf-8. '
                    'Save the contents of the file to disk instead.'
                ) from e
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
            profile = self.escape_profile_element(p['app_name'])
            profile += '/'

            if not p['2_part_profile_format_allowed']:
                profile += self.escape_profile_element(p['env_name'])
                profile += '/'

            profile += self.escape_profile_element(p['profile_name'])
            profiles.append(profile)
        Cache().save_profiles(profiles)

    @staticmethod
    def escape_profile_element(element):
        return element.replace('/', '\\/')

    @staticmethod
    def cache_clear():
        Cache().clear()

    def configure_update(self, section, field, value):
        self.config.update(section=section, field=field, value=value)

    def request_submit(self, profile, justification):
        self._validate_justification(justification)
        self.login()
        parts = self._split_profile_into_parts(profile)

        ids = self._convert_names_to_ids(
            profile_name=parts['profile'],
            environment_name=parts['env'],
            application_name=parts['app']
        )

        self.b.my_access.request_approval(
            profile_id=ids['profile_id'],
            environment_id=ids['environment_id'],
            block_until_disposition=False,
            justification=justification
        )

    def request_withdraw(self, profile):
        self.login()
        parts = self._split_profile_into_parts(profile)

        ids = self._convert_names_to_ids(
            profile_name=parts['profile'],
            environment_name=parts['env'],
            application_name=parts['app']
        )

        self.b.my_access.withdraw_approval_request(
            profile_id=ids['profile_id'],
            environment_id=ids['environment_id']
        )

    def clear_gcloud_auth_key_files(self):
        self.config.clear_gcloud_auth_key_files()

    def api(self, method, parameters: dict, query=None):
        self.login()

        # clean up parameters - need to load json as dict if json string is provided and handle file inputs
        computed_parameters = {}
        open_file_keys = []
        try:
            for key, value in parameters.items():
                computed_key = key.replace('-', '_')
                computed_value = value

                if value.lower() == 'none':
                    computed_value = None

                if value.startswith('file://'):
                    filepath = value.replace('file://', '')
                    path = pathlib.Path(filepath)
                    with open(str(path), 'r', encoding='utf-8') as f:
                        computed_value = f.read().strip()

                if value.startswith('fileb://'):
                    filepath = value.replace('fileb://', '')
                    path = pathlib.Path(filepath)
                    computed_value = open(str(path), 'rb')
                    open_file_keys.append(computed_key)

                try:
                    computed_parameters[computed_key] = json.loads(computed_value)
                except json.JSONDecodeError:
                    computed_parameters[computed_key] = computed_value
                except Exception:  # not sure what else we would do so just default to the value provided
                    computed_parameters[computed_key] = computed_value
        except AttributeError as e:
            raise click.ClickException(f'invalid parameters {parameters} provided.') from e

        # determine the sdk method we need to execute, starting at the base Britive class
        func = self.b
        try:
            for m in method.split('.'):
                func = getattr(func, m)
        except Exception as e:
            raise click.ClickException(f'invalid method {method} provided.') from e

        # execute the method with the computed parameters
        response = func(**computed_parameters)

        # close any files we opened due to fileb:// prefix
        for key in open_file_keys:
            try:
                computed_parameters[key].close()
            except Exception:
                pass

        # output the response, optionally filtering based on provided jmespath query/search
        self.print(jmespath.search(query, response) if query else response, ignore_silent=True)

    # yes - this method exits in b.my_access as _get_profile_and_environment_ids_given_names
    # but we are doing additional business logic here to enhance the cli experience so there is
    # a need to duplicate some of this logic (although we are doing additional work here so the logic is
    # not 100% duplicated)
    def _convert_names_to_ids(self, profile_name: str, environment_name: str, application_name: str) -> dict:
        # set the available profiles if this is not already done
        self._set_available_profiles()

        # do some sanitization just in case
        profile_name = profile_name.lower().strip()
        environment_name = environment_name.lower().strip()
        application_name = application_name.lower().strip()

        found_profiles = {}

        # collect relevant profile/environment combinations to which the identity is entitled
        for profile in self.available_profiles:
            if profile['app_name'].lower() != application_name:  # kick out all the unmatched applications
                continue
            if profile['profile_name'].lower() != profile_name:  # kick out the unmatched profiles
                continue

            # if we get here we know we are on a record that is the right app and right profile

            found_profile_id = profile['profile_id']

            if found_profile_id not in found_profiles:
                found_profiles[found_profile_id] = []

            # load up multiple options
            env_options = [
                profile['env_name'].lower(),
                profile['env_id'].lower(),
                profile['env_short_name'].lower()
            ]

            if environment_name in env_options:
                found_profiles[found_profile_id].append(profile['env_id'])

        # let's first check to ensure we have only 1 profile
        if len(found_profiles) == 0:
            raise click.ClickException('no profile found with the provided application, environment, and profile names')
        if len(found_profiles) > 1:
            raise click.ClickException('multiple matching profiles found - cannot determine which profile to use')

        # and now we can check to ensure we have only 1 environment
        found_profile_id = list(found_profiles)[0]
        possible_environments = found_profiles[found_profile_id]
        if len(possible_environments) == 0:
            raise click.ClickException('no profile found with the provided application, environment, and profile names')
        if len(possible_environments) > 1:
            raise click.ClickException('multiple matching profiles found - cannot determine which profile to use')

        return {
            'profile_id': found_profile_id,
            'environment_id': possible_environments[0]
        }

    @staticmethod
    def _validate_justification(justification: str):
        if justification and len(justification) > 255:
            raise ValueError('justification cannot be longer than 255 characters.')

    def ssh_aws_ssm_proxy(self, username, hostname, push_public_key, port_number, key_source):
        self.silent = True
        helper = hostname.split('.')
        instance_id = helper[0]
        aws_profile = None  # will drop to using standard aws boto3/cli profile provider chain
        aws_region = None  # will drop to using standard aws boto3/cli region provider chain
        if len(helper) > 1:
            aws_profile = helper[1]
        if len(helper) > 2:
            aws_region = helper[2]

        if push_public_key:
            details = self._ssh_generate_key(
                username=username,
                hostname=hostname,
                key_source=key_source
            )
            self._ssh_aws_push_key(
                instance_id=instance_id,
                aws_profile=aws_profile,
                aws_region=aws_region,
                username=username,
                key_pair=details['key_pair']
            )

        commands = [
            'aws',
            'ssm',
            'start-session',
            f'--parameters portNumber={port_number}',
            '--document-name AWS-StartSSHSession',
            f'--target {instance_id}'
        ]

        if aws_profile:
            commands.append(f'--profile {aws_profile}')
        if aws_region:
            commands.append(f'--region {aws_region}')

        self.print(' '.join(commands), ignore_silent=True)

    @staticmethod
    def _ssh_generate_key_pair():
        # doing imports here as these packages are not a requirement to use pybritive in general
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        pem_public_key = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )

        return {
            'private': pem_private_key,
            'public': pem_public_key
        }

    def _ssh_generate_key(self, username, hostname, key_source):
        # doing imports here as these packages are not a requirement to use pybritive in general

        # these 3 ship with python3.x
        import glob
        import time
        import subprocess

        key_pair = self._ssh_generate_key_pair()

        # let's do the right thing and clean up old ephemeral keys
        ssh_dir = Path(self.config.path).parent.absolute() / 'ssh'
        ssh_dir.mkdir(exist_ok=True, parents=True)  # create the directory if it doesn't exist already
        if key_source == 'ssh-agent':
            # cleanup any old ssh keys that were randomly generated
            now = int(time.time())
            for key in glob.glob(f'{str(ssh_dir)}/random-*'):
                file = key.split('/')[-1].split('.')[0]
                expiration = int(file.split('-')[2])
                if expiration < now:
                    Path(key).unlink(missing_ok=True)

            pem_file = ssh_dir / f'random-{uuid.uuid4().hex}-{now + 60}.pem'
        elif key_source == 'static':
            # clean up the specific key if it exists, so we can create a new one
            pem_file = ssh_dir / f'{hostname}.{username}.pem'
            pem_file.unlink(missing_ok=True)
        else:
            raise ValueError(f'invalid --key-source value {key_source}')

        # we only need to persist the private key locally
        # as the public key is just pushed to the ec2 instance
        # as a string in the ec2 instance connect api call (no file
        # reference)
        with open(str(pem_file), 'w', encoding='utf-8') as f:
            f.write(key_pair['private'].decode())
        os.chmod(pem_file, 0o400)

        # and if we are using ssh-agent we need to add the private key via ssh-add
        if key_source == 'ssh-agent':
            subprocess.run(['ssh-add', '-t', '60', '-q', str(pem_file)], check=False)

        return {
            'private_key_filename': pem_file,
            'key_pair': key_pair
        }

    @staticmethod
    def _ssh_aws_push_key(aws_profile, aws_region, instance_id, username, key_pair):
        try:
            import boto3
        except ImportError as e:
            message = 'boto3 package is required. Please ensure the package is installed.'
            raise click.ClickException(message) from e

        # we know we will be pushing the key to the instance so establish the
        # boto3 clients which are required to perform those actions
        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        eic = session.client('ec2-instance-connect')
        ec2 = session.client('ec2')

        # now push the key
        az = ec2.describe_instances(
            InstanceIds=[instance_id]
        )['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']

        eic.send_ssh_public_key(
            InstanceId=instance_id,
            InstanceOSUser=username,
            SSHPublicKey=key_pair['public'].decode(),
            AvailabilityZone=az
        )

    def ssh_aws_openssh_config(self, push_public_key, key_source):
        lines = ['Match host i-*,mi-*']
        if push_public_key:
            commands = [
                '\tProxyCommand eval $(pybritive ssh aws ssm-proxy --hostname %h',
                '--username %r --port-number %p --push-public-key',
                f'--key-source {key_source})'
            ]
            lines.append(' '.join(commands))

            if key_source == 'static':
                ssh_dir = Path(self.config.path).parent.absolute() / 'ssh'
                lines.append(f'\tIdentityFile {str(ssh_dir)}/%h.%r.pem')
        else:
            line = '\tProxyCommand eval $(pybritive ssh aws ssm-proxy --hostname %h --username %r --port-number %p)'
            lines.append(line)

        self.print('Add the below Match directive to your SSH config file, after all Host directives.')
        self.print('This file is generally located at ~/.ssh/config.')
        self.print('Additional SSH config parameters can be added as required.')
        self.print('The below directive is the minimum required configuration.')
        self.print('')
        self.print('')
        self.print('\n'.join(lines))

    @staticmethod
    def aws_console(profile, duration, browser):
        # doing imports here as these packages are not a requirement to use pybritive in general

        # requests is a hard requirement for pybritive (via britive sdk)
        # and webbrowser ships with python3.x
        import requests
        import webbrowser

        # this is the one that may not be available so be careful
        try:
            import boto3
        except ImportError as e:
            message = 'boto3 package is required. Please ensure the package is installed.'
            raise click.ClickException(message) from e

        creds = boto3.Session(profile_name=profile).get_credentials()
        session_id = creds.access_key
        session_key = creds.secret_key
        session_token = creds.token
        json_creds = json.dumps({
            'sessionId': session_id,
            'sessionKey': session_key,
            'sessionToken': session_token
        })

        # Make request to AWS federation endpoint to get sign-in token. Construct the parameter string with
        # the sign-in action request and the JSON document with temporary credentials as parameters.

        params = {
            'Action': 'getSigninToken',
            'SessionDuration': duration,
            'Session': json_creds
        }

        url = 'https://signin.aws.amazon.com/federation'

        response = requests.get(url, params=params)

        signin_token = None
        try:
            signin_token = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            click.ClickException('Credentials have expired or another issue occurred. '
                                 'Please re-authenticate and try again.')

        params = {
            'Action': 'login',
            'Issuer': 'pybritive',
            'Destination': 'https://console.aws.amazon.com/',
            'SigninToken': signin_token['SigninToken']
        }

        # using requests.prepare() here to  help construct the url (with url encoding, etc.)
        # vs. doing it "manually" - we do not want to actually make a request to the url in python
        # but use the url to pop open a browser
        console_url = requests.Request('GET', url, params=params).prepare().url

        webbrowser.get(using=browser).open(console_url)

    def request_disposition(self, request_id, decision):
        self.login()

        if decision == 'approve':
            self.b.my_access.approve_request(request_id=request_id)
        if decision == 'reject':
            self.b.my_access.reject_request(request_id=request_id)

    def clear_cached_aws_credentials(self, profile):
        # start with the profile name that was passed in from the command
        Cache().clear_awscredentialprocess(profile_name=profile)

        # then we can try to split it into parts and clear that version of the
        # profile name as well - it will not hurt anything to try to clear
        # both versions
        parts = self._split_profile_into_parts(profile)
        Cache().clear_awscredentialprocess(profile_name=f"{parts['app']}/{parts['env']}/{parts['profile']}")

    def ssh_gcp_identity_aware_proxy(self, username, hostname, push_public_key, port_number, key_source):
        self.silent = True
        helper = hostname.split('.')
        instance_name = helper[1]
        project = helper[2]

        import subprocess
        import shlex

        command = f'gcloud compute instances list --format json --project {project}'
        instances = json.loads(subprocess.check_output(shlex.split(command)).decode('utf-8'))

        zone = None
        metadata = None
        for instance in instances:
            if instance['name'] == instance_name:
                zone = instance['zone'].split('/')[-1]
                metadata = instance.get('metadata')

        if not zone:
            raise click.BadParameter(f'no zone found for instance {instance_name} in project {project}')

        if push_public_key:
            details = self._ssh_generate_key(
                username=username,
                hostname=hostname,
                key_source=key_source
            )

            if push_public_key == 'os-login':  # this is pretty straightforward
                public_key = details["key_pair"]["public"].decode('utf-8')
                command = f'gcloud compute os-login ssh-keys add --key="{public_key}" ' \
                          f'--project={project} --ttl=1m --no-user-output-enabled --quiet'
                subprocess.check_output(shlex.split(command))
            if push_public_key == 'instance-metadata':  # this is a bit more involved
                now = datetime.now(timezone.utc).replace(microsecond=0)

                if metadata:
                    existing_keys_str = None
                    for item in metadata.get('items', []):
                        if item['key'] == 'ssh-keys':
                            existing_keys_str = item['value']
                            break
                    future_keys = []
                    if existing_keys_str:
                        existing_keys = existing_keys_str.split('\n')

                        for key in existing_keys:
                            should_carry_forward = True

                            if 'google-ssh' in key:  # non google-ssh keys should always carry forward
                                key_details = json.loads(key.split('google-ssh')[1].strip())
                                expires = key_details['expireOn']
                                if now > datetime.fromisoformat(expires):
                                    should_carry_forward = False
                            if should_carry_forward:
                                future_keys.append(key)

                    command = 'gcloud auth list --filter=status:ACTIVE --format="value(account)" --quiet'
                    active_gcloud_user = subprocess.check_output(shlex.split(command)).decode('utf-8').strip()

                    # format is 2023-05-16T20:15:22+0000
                    google_ssh_data = {
                        'userName': active_gcloud_user,
                        'expireOn': (now + timedelta(seconds=60)).strftime('%Y-%m-%dT%H:%M:%S+0000')
                    }
                    google_ssh_data = json.dumps(google_ssh_data, separators=(',', ':'))  # separators IMPORTANT
                    public_key = details["key_pair"]["public"].decode('utf-8')
                    new_key = f'{username}:{public_key} google-ssh {google_ssh_data}'
                    future_keys.append(new_key)

                    ssh_dir = Path(self.config.path).parent.absolute() / 'ssh'
                    ssh_dir.mkdir(exist_ok=True, parents=True)  # create the directory if it doesn't exist already
                    key_file = ssh_dir / uuid.uuid4().hex
                    with open(str(key_file), 'w', encoding='utf-8') as f:
                        f.write('\n'.join(future_keys))

                    commands = [
                        'gcloud',
                        'compute',
                        'instances',
                        'add-metadata',
                        instance_name,
                        '--project',
                        project,
                        '--metadata-from-file',
                        f'ssh-keys={str(key_file)}',
                        '--zone',
                        zone,
                        '--verbosity=error',
                        '--no-user-output-enabled',
                        '--quiet'
                    ]
                    subprocess.run(commands, check=False)
                    key_file.unlink(missing_ok=True)

        commands = [
            'gcloud',
            'compute',
            'start-iap-tunnel',
            instance_name,
            port_number,
            '--listen-on-stdin',
            f'--project={project}',
            f'--zone={zone}',
            '--verbosity=error'
        ]

        self.print(' '.join(commands), ignore_silent=True)

    def ssh_gcp_openssh_config(self, push_public_key, key_source):
        lines = ['Match host gcp.*']
        if push_public_key:
            commands = [
                '\tProxyCommand eval $(pybritive gcp identity-aware-proxy --hostname %h',
                f'--username %r --port-number %p --push-public-key {push_public_key}',
                f'--key-source {key_source})'
            ]
            lines.append(' '.join(commands))

            if key_source == 'static':
                ssh_dir = Path(self.config.path).parent.absolute() / 'ssh'
                lines.append(f'\tIdentityFile {str(ssh_dir)}/%h.%r.pem')
        else:
            line = '\tProxyCommand eval $(pybritive ssh gcp identity-aware-proxy --hostname %h --username %r ' \
                   '--port-number %p)'
            lines.append(line)

        self.print('Add the below Match directive to your SSH config file, after all Host directives.')
        self.print('This file is generally located at ~/.ssh/config.')
        self.print('Additional SSH config parameters can be added as required.')
        self.print('The below directive is the minimum required configuration.')
        self.print('')
        self.print('')
        self.print('\n'.join(lines))
