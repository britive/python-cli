import configparser
import json
import os
import subprocess
from pathlib import Path
import platform
import uuid
import webbrowser
import click


# trailing spaces matter as some options do not have the trailing space
env_options = {
    'nix': 'export ',
    'winps': '$Env:',
    'wincmd': 'set '
}


def safe_list_get(l, idx, default):
    try:
        return l[idx]
    except IndexError:
        return default


class CloudCredentialPrinter:
    def __init__(self, app_type, console, mode, profile, silent, credentials, cli):
        self.cli = cli
        self.silent = silent
        self.app_type = app_type
        self.profile = profile
        self.console = console
        mode = mode or 'json'  # set a default if nothing is provided via flag --mode/-m
        self.full_mode = mode
        helper = mode.split('-')
        self.mode = helper[0]
        self.mode_modifier = safe_list_get(mode.split('-', maxsplit=1), 1, None)
        self.credentials = credentials
        if self.mode == 'env':
            if self.mode_modifier:
                self.env_command = env_options[self.mode_modifier]
            else:
                self.on_windows = platform.system().lower() == 'windows'
                self.env_command = env_options['wincmd'] if self.on_windows else env_options['nix']
        self.modes_to_skip_console_printing = ['os-oclogin', 'os-ocloginexec']

    def print(self):
        if self.console and self.full_mode not in self.modes_to_skip_console_printing:
            self.print_console()
            return
        if self.mode == 'text':
            self.print_text()
        if self.mode == 'json':
            self.print_json()
        if self.mode == 'env':
            self.print_env()
        if self.mode == 'integrate':
            self.print_integrate()
        if self.mode == 'azlogin':
            self.print_azlogin()
        if self.mode == 'awscredentialprocess':
            self.print_awscredentialprocess()
        if self.mode == 'azps':
            self.print_azps()
        if self.mode == 'gcloudauth':
            self.print_gcloudauth()
        if self.mode == 'kube':
            self.print_kube()
        if self.mode == 'os':
            self.print_os()
        if self.mode == 'gcloudauthexec':
            self.print_gcloudauthexec()

    def print_console(self):
        url = self.credentials.get('url', self.credentials)
        if self.mode == 'browser':
            browser = self.mode_modifier or os.getenv('PYBRITIVE_BROWSER')
            webbrowser.get(using=browser).open(url)
        else:
            self.cli.print(url, ignore_silent=True)

    def print_text(self):
        self._not_implemented()

    def print_json(self):
        self._not_implemented()

    def print_env(self):
        self._not_implemented()

    def print_integrate(self):
        self._not_implemented()

    def print_awscredentialprocess(self):
        self._not_implemented()

    def print_azlogin(self):
        self._not_implemented()

    def print_azps(self):
        self._not_implemented()

    def print_gcloudauth(self):
        self._not_implemented()

    def print_kube(self):
        self._not_implemented()

    def print_gcloudauthexec(self):
        self._not_implemented()

    def print_os(self):
        self._not_implemented()

    def _not_implemented(self):
        raise click.ClickException(f'Application type {self.app_type} does not support the specified mode.')


class GenericCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, silent, credentials, cli):
        super().__init__('Generic', console, mode, profile, silent, credentials, cli)

    def print_json(self):
        try:
            self.cli.print(json.dumps(self.credentials, indent=2), ignore_silent=True)
        except json.JSONDecodeError:
            self.cli.print(self.credentials, ignore_silent=True)


class ResourcesCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, profile, silent, credentials, cli):
        super().__init__('Resources', False, 'text', profile, silent, credentials, cli)

    def print_text(self):
        self.cli.print(self.credentials, ignore_silent=True)


class AwsCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, silent, credentials, cli, aws_credentials_file):
        super().__init__('AWS', console, mode, profile, silent, credentials, cli)
        self.aws_credentials_file = aws_credentials_file

    def print_text(self):
        self.cli.print('AWS_ACCESS_KEY_ID', ignore_silent=True)
        self.cli.print(self.credentials['accessKeyID'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

        self.cli.print('AWS_SECRET_ACCESS_KEY', ignore_silent=True)
        self.cli.print(self.credentials['secretAccessKey'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

        self.cli.print('AWS_SESSION_TOKEN', ignore_silent=True)
        self.cli.print(self.credentials['sessionToken'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

        self.cli.print('AWS_EXPIRATION', ignore_silent=True)
        self.cli.print(self.credentials['expirationTime'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

    def print_json(self, version=None):
        creds = {
            'AccessKeyId': self.credentials['accessKeyID'],
            'SecretAccessKey': self.credentials['secretAccessKey'],
            'SessionToken': self.credentials['sessionToken'],
            'Expiration': self.credentials['expirationTime']
        }
        if version:
            creds['Version'] = version
        self.cli.print(json.dumps(creds, indent=2), ignore_silent=True)

    def print_env(self):
        self.cli.print(f'{self.env_command}AWS_ACCESS_KEY_ID="{self.credentials["accessKeyID"]}"', ignore_silent=True)
        self.cli.print(f'{self.env_command}AWS_SECRET_ACCESS_KEY="{self.credentials["secretAccessKey"]}"',
                       ignore_silent=True)
        self.cli.print(f'{self.env_command}AWS_SESSION_TOKEN="{self.credentials["sessionToken"]}"', ignore_silent=True)
        self.cli.print(f'{self.env_command}AWS_EXPIRATION="{self.credentials["expirationTime"]}"', ignore_silent=True)

    def print_integrate(self):
        # get path to aws credentials file
        env_path = self.aws_credentials_file
        if not env_path:
            path = Path.home() / '.aws' / 'credentials'  # handle os specific separators properly
        else:
            path = Path(env_path)

        # if credentials file does not yet exist, create it as an empty file
        if not path.is_file():
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('', encoding='utf-8')

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
        with open(str(path), 'w', encoding='utf-8') as f:
            config.write(f, space_around_delimiters=False)

    def print_awscredentialprocess(self):
        self.print_json(version=1)


class AzureCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, silent, credentials, cli):
        key = list(credentials.keys())[0]
        if key != 'url':  # console url is handled differently than programmatic keys so account for it here
            credentials = json.loads(credentials[key])
        super().__init__('Azure', console, mode, profile, silent, credentials, cli)

    def print_text(self):
        self.cli.print('TENANT', ignore_silent=True)
        self.cli.print(self.credentials['tenantId'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

        self.cli.print('USERNAME/APP ID/CLIENT ID', ignore_silent=True)
        self.cli.print(self.credentials['appId'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

        self.cli.print('PASSWORD/SECRET TEXT/CLIENT SECRET', ignore_silent=True)
        self.cli.print(self.credentials['secretText'], ignore_silent=True)
        self.cli.print('', ignore_silent=True)

    def print_json(self):
        creds = {
            'TenantId': self.credentials['tenantId'],
            'ClientId': self.credentials['appId'],
            'ClientSecret': self.credentials['secretText']
        }
        self.cli.print(json.dumps(creds, indent=2), ignore_silent=True)

    def print_env(self):
        self.cli.print(f'{self.env_command}AZURE_CLIENT_ID="{self.credentials["appId"]}"', ignore_silent=True)
        self.cli.print(f'{self.env_command}AZURE_CLIENT_SECRET="{self.credentials["secretText"]}"', ignore_silent=True)
        self.cli.print(f'{self.env_command}AZURE_TENANT_ID="{self.credentials["tenantId"]}"', ignore_silent=True)

    def print_azlogin(self):
        self.cli.print(self.credentials['cliLogin'], ignore_silent=True)

    def print_azps(self):
        self.cli.print(self.credentials['powershellScript'].replace('\n ', '\n'), ignore_silent=True)


class GcpCloudCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, silent, credentials, cli, gcloud_key_file):
        key = list(credentials.keys())[0]
        credentials = json.loads(credentials[key]) if key != 'url' else credentials
        super().__init__('GCP', console, mode, profile, silent, credentials, cli)
        self.gcloud_key_file = gcloud_key_file

    def print_json(self):
        self.cli.print(json.dumps(self.credentials, indent=2), ignore_silent=True)
        self.cli.print('', ignore_silent=True)
        self.cli.print(
            f"Run command: gcloud auth activate-service-account {self.credentials['client_email']} "
            "--key-file <path-where-above-json-is-stored>", ignore_silent=True
        )

    def print_gcloudauth(self):
        # get path to gcloud key file
        if not self.gcloud_key_file:  # if --gcloud-key-file not provided
            path = Path(self.cli.config.gcloud_key_file_path) / f'{uuid.uuid4().hex}.json'
        else:  # we need to parse out/sanitize what was provided
            path = Path(self.gcloud_key_file).expanduser().absolute()

        # key file does not yet exist so write to it
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(json.dumps(self.credentials, indent=2), encoding='utf-8')

        self.cli.print(
            f"gcloud auth activate-service-account {self.credentials['client_email']} --key-file {str(path)}",
            ignore_silent=True
        )

    def print_gcloudauthexec(self):
        key_file = self.cli.build_gcloud_key_file_for_gcloudauthexec(profile=self.profile)
        path = Path(self.cli.config.gcloud_key_file_path) / key_file

        # key file does not yet exist so write to it
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(json.dumps(self.credentials, indent=2), encoding='utf-8')

        try:
            commands = [
                'gcloud',
                'auth',
                'activate-service-account',
                self.credentials['client_email'],
                '--key-file',
                str(path),
                '--verbosity=error'
            ]

            subprocess.run(commands, check=True)
        except Exception as e:
            self.cli.print(f'error running `gcloud auth activate-service-account ...`: {str(e)}')


class KubernetesCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, silent, credentials, cli, k8s_processor):
        self.k8s_processor = k8s_processor
        super().__init__('Kubernetes', console, mode, profile, silent, credentials, cli)

    def print_json(self):
        try:
            self.cli.print(json.dumps(self.credentials, indent=2), ignore_silent=True)
        except json.JSONDecodeError:
            self.cli.print(self.credentials, ignore_silent=True)

    def print_kube(self):
        if self.mode_modifier == 'exec':
            self.cli.print(self.k8s_processor.construct_exec_credential(self.credentials), ignore_silent=True)
        else:
            raise ValueError(f'--mode modifier {self.mode_modifier} for mode {self.mode} not supported')


class OpenShiftCredentialPrinter(CloudCredentialPrinter):
    def __init__(self, console, mode, profile, silent, credentials, cli):
        super().__init__('OpenShift', console, mode, profile, silent, credentials, cli)

    def print_json(self):
        try:
            self.cli.print(json.dumps(self.credentials, indent=2), ignore_silent=True)
        except json.JSONDecodeError:
            self.cli.print(self.credentials, ignore_silent=True)

    def _perform_oidc_auth_code_grant_flow(self):
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib.parse import urlparse

            try:
                from bs4 import BeautifulSoup
            except ImportError as e:
                raise click.ClickException(self.cli.build_import_exception_message('openshift')) from e

            class BritiveCustomHeaderAdapter(HTTPAdapter):
                def __init__(self, headers=None, *args, **kwargs):
                    self.headers = headers or {}
                    super().__init__(*args, **kwargs)

                def add_headers(self, request, **kwargs):
                    for h, v in self.headers.items():
                        request.headers.setdefault(h, v)

            sdk_headers = self.cli.b.session.headers
            tenant_fqdn = self.cli.b.tenant
            temp_url = self.credentials['url']
            temp_url = temp_url.replace('console-openshift-console', 'oauth-openshift')
            parsed_url = urlparse(temp_url)
            base_url = parsed_url.scheme + "://" + parsed_url.netloc
            idp = self.credentials['idpName']

            session = requests.session()

            # set a reasonable user agent, so we can identify traffic more easily
            session.headers.update({
                'User-Agent': sdk_headers['User-Agent']
            })

            # create a custom adapter for the tenants fqdn and mount it
            # this will include the authorization header, so we can "auto"
            # authenticate to the tenant
            adapter = BritiveCustomHeaderAdapter(headers={'Authorization': sdk_headers['Authorization']})
            session.mount(f'https://{tenant_fqdn}/', adapter)

            token_request_url = f'{base_url}/oauth/token/request'
            idp_selection_url = session.get(token_request_url, allow_redirects=False).headers['Location']
            idp_selected_url = f'{idp_selection_url}&idp={idp}'
            response = session.get(idp_selected_url, allow_redirects=True)
            # we now have a html file that we need to extract some things from
            soup = BeautifulSoup(response.content, 'html.parser')
            input_values = {}
            form = soup.find('form')
            inputs = form.find_all('input')
            for inp in inputs:
                name = inp.get('name')
                value = inp.get('value')
                if name:
                    input_values[name] = value

            form_action = form['action']
            if form_action.startswith('/'):
                form_action = form_action[1:]
            response = session.post(f'{base_url}/{form_action}', data=input_values)

            # and we get more html content we need to parse now
            soup = BeautifulSoup(response.content, 'html.parser')

            command = None
            for line in soup.get_text().split('\n'):
                if line.startswith('oc login'):
                    command = line
                    break

            if command:
                return command
            else:
                raise Exception(f'error: no `oc login` command found')
        except Exception as e:
            self.cli.print(f'error when attempting to perform oidc auth code grant flow: {str(e)}', ignore_silent=True)

    def print_os(self):
        if self.mode_modifier == 'oclogin':
            command = self._perform_oidc_auth_code_grant_flow()
            self.cli.print(command, ignore_silent=True)
        elif self.mode_modifier == 'ocloginexec':
            command = self._perform_oidc_auth_code_grant_flow()
            try:
                subprocess.run(command.split(' '), check=True)
            except Exception as e:
                self.cli.print(f'error running `gcloud auth activate-service-account ...`: {str(e)}')
        else:
            raise ValueError(f'--mode modifier {self.mode_modifier} for mode {self.mode} not supported')
