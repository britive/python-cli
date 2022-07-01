import random
import base64
import hashlib
import webbrowser
import time
import requests
from pathlib import Path
import yaml
import typer


interactive_login_fields_to_pop = [
    'challengeParameters',
    'success',
    'type',
    'user',
    'userId',
    'username',
    'refreshToken',
    'authTime',
    'maxSessionTimeout'
]


# the credentials should expire sooner than the true expiration date
# in case we need to do things like polling for credentials during
# an approval process
credential_expiration_safe_zone_minutes = 10


class InteractiveLoginTimeout(Exception):
    pass


def b64_encode_url_safe(value: bytes):
    return base64.urlsafe_b64encode(value).decode('utf-8').replace('=', '')


class CredentialManager:
    def __init__(self, tenant_name: str, tenant_alias: str):
        self.tenant = tenant_name
        self.alias = tenant_alias
        self.base_url = f'https://{self.tenant}.britive-app.com'

        # not sure if we really need 32 random bytes or if any random string would work
        # but the current britive-cli in node.js does it this way so it will be done the same
        # way in python
        self.verifier = b64_encode_url_safe(bytes([random.getrandbits(8) for _ in range(0, 32)]))
        self.auth_token = b64_encode_url_safe(bytes(hashlib.sha512(self.verifier.encode('utf-8')).digest()))
        self.credentials = self.load() or {}

    def perform_interactive_login(self):
        typer.echo(f'Performing interacive login against tenant {self.tenant}')
        url = f'{self.base_url}/login?token={self.auth_token}'
        webbrowser.get().open(url)
        time.sleep(3)
        num_tries = 1
        while True:
            if num_tries > 60:
                raise InteractiveLoginTimeout()
            response = self.retrieve_tokens()

            if response.status_code >= 400:
                time.sleep(2)
                num_tries += 1
            else:
                credentials = response.json()['authenticationResult']

                # calculate a safe expiration time
                auth_time = int(credentials.get('authTime', 0))
                session_time = int(credentials.get('maxSessionTimeout', 0))
                creds_expire_after = auth_time + session_time - (credential_expiration_safe_zone_minutes * 60 * 1000)
                credentials['safeExpirationTime'] = creds_expire_after

                # drop a bunch of unnecessary fields
                for field in interactive_login_fields_to_pop:
                    credentials.pop(field, None)

                self.save(credentials)
                typer.echo(f'Authenticated to tenant {self.tenant} via interactive login.')
                break

    def retrieve_tokens(self):
        url = f'{self.base_url}/api/auth/cli/retrieve-tokens'
        auth_params = {
            'authParameters': {
                'cliToken': self.verifier
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        return requests.post(url, headers=headers, json=auth_params)

    def load(self, full=False):
        # we should NEVER here exception but adding here just in case
        typer.echo('Must use a subclass of CredentialManager')
        raise typer.Abort()

    def save(self, credentials: dict):
        # we should NEVER get here but adding here just in case
        typer.echo('Must use a subclass of CredentialManager')
        raise typer.Abort()

    def delete(self):
        # we should NEVER get here but adding here just in case
        typer.echo('Must use a subclass of CredentialManager')
        raise typer.Abort()

    def get_credentials(self):
        if self.has_valid_credentials():
            return self.credentials
        else:  # no credentials or expired creds for the given tenant so perform interactive login
            self.perform_interactive_login()  # will write the credentials out and update self.credentials as needed
            return self.credentials

    def get_token(self):
        return self.get_credentials()['accessToken']

    def has_valid_credentials(self):
        if not self.credentials or self.credentials == {}:
            typer.echo(f'Credentials for tenant {self.tenant} not found.')
            return False
        if int(time.time() * 1000) <= int(self.credentials.get('safeExpirationTime', 0)):
            return True
        typer.echo(f'Credentials for tenant {self.tenant} have expired.')
        return False


class FileCredentialManager(CredentialManager):
    def __init__(self, tenant_name: str, tenant_alias: str):
        self.path = str(Path.home() / '.pybritive' / 'credentials.yaml')
        super().__init__(tenant_name, tenant_alias)

    def load(self, full=False):
        path = Path(self.path)
        if not path.is_file():  # credentials file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

        # now load the credentials file
        with open(self.path, 'r') as f:
            try:
                credentials = yaml.safe_load(f) or {}
                if full:
                    return credentials
                return credentials.get(self.tenant, None)
            except yaml.YAMLError:
                typer.echo(f'Invalid YAML file at {self.path}')
                raise typer.Abort()

    def save(self, credentials: dict):
        full_credentials = self.load(full=True)
        if credentials is None:
            full_credentials.pop(self.alias, None)
        else:
            full_credentials[self.alias] = credentials
        with open(self.path, 'w') as f:
            f.write(yaml.safe_dump(full_credentials))
        self.credentials = credentials

    def delete(self):
        self.save(None)





