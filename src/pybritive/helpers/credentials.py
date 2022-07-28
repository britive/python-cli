import random
import base64
import hashlib
import time
import requests
from pathlib import Path
import click
import configparser
import json
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .config import ConfigManager
import uuid
import os


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


# this base class expects self.credentials to be a dict - so sub classes need to convert to dict
class CredentialManager:
    def __init__(self, tenant_name: str, tenant_alias: str, cli: ConfigManager):
        self.cli = cli
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
        self.cli.print(f'Performing interactive login against tenant {self.tenant}')
        url = f'{self.base_url}/login?token={self.auth_token}'
        click.launch(url)
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
                self.cli.print(f'Authenticated to tenant {self.tenant} via interactive login.')
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
        raise click.ClickException('Must use a subclass of CredentialManager')

    def save(self, credentials: dict):
        # we should NEVER get here but adding here just in case
        raise click.ClickException('Must use a subclass of CredentialManager')

    def delete(self):
        # we should NEVER get here but adding here just in case
        raise click.ClickException('Must use a subclass of CredentialManager')

    # this helper exists since subclasses may need to override the method due to how the
    # access token may be encrypted and/or stored
    def _get_token(self):
        return self.credentials['accessToken']

    def get_token(self):
        if not self.has_valid_credentials():  # no credentials or expired creds for the  tenant so do interactive login
            self.perform_interactive_login()  # will write the credentials out and update self.credentials as needed
        return self._get_token()

    def has_valid_credentials(self):
        if not self.credentials or self.credentials == {}:
            self.cli.print(f'Credentials for tenant {self.tenant} not found.')
            return False
        if int(time.time() * 1000) <= int(self.credentials.get('safeExpirationTime', 0)):
            return True
        self.cli.print(f'Credentials for tenant {self.tenant} have expired.')
        return False


class FileCredentialManager(CredentialManager):
    def __init__(self, tenant_name: str, tenant_alias: str, cli: ConfigManager):
        self.path = str(Path.home() / '.britive' / 'pybritive.credentials')
        super().__init__(tenant_name, tenant_alias, cli)

    def load(self, full=False):
        path = Path(self.path)
        if not path.is_file():  # credentials file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

        # open the file with configparser
        credentials = configparser.ConfigParser()
        credentials.optionxform = str  # maintain key case
        credentials.read(str(path))
        credentials = json.loads(json.dumps(credentials._sections))  # TODO this is messy but works for now
        if full:
            return credentials
        return credentials.get(self.alias, None)

    def save(self, credentials: dict):
        full_credentials = self.load(full=True)
        if credentials is None:
            full_credentials.pop(self.alias, None)
        else:
            full_credentials[self.alias] = credentials

        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read_dict(full_credentials)

        # write the new credentials file
        with open(str(self.path), 'w') as f:
            config.write(f, space_around_delimiters=False)
        self.credentials = credentials

    def delete(self):
        self.save(None)


class EncryptedFileCredentialManager(CredentialManager):
    def __init__(self, tenant_name: str, tenant_alias: str, cli: ConfigManager, passphrase: str = None):
        self.path = str(Path.home() / '.britive' / 'pybritive.credentials.encrypted')
        self.passphrase = passphrase
        self.prompt()
        super().__init__(tenant_name, tenant_alias, cli)

    @staticmethod
    def salt():
        return base64.b64encode(os.urandom(32)).decode('utf-8')

    def key(self, salt: str):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=base64.b64decode(salt.encode()),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.passphrase.encode()))
        return key

    def prompt(self):
        if not self.passphrase:
            self.passphrase = click.prompt(
                'Enter passphrase to be used to encrypt/decrypt the credentials file',
                hide_input=True
            )

    def decrypt(self, encrypted_access_token: str):
        try:
            encrypted_access_token, b64salt = encrypted_access_token.split(':')
            key = self.key(b64salt)
            return Fernet(key).decrypt(base64.b64decode(encrypted_access_token.encode())).decode('utf-8')
        except InvalidToken:
            raise click.ClickException('Invalid passphrase provided. Unable to decrypt credentials.')

    def encrypt(self, decrypted_access_token: str):
        salt = self.salt()
        key = self.key(salt)
        encrypted_access_token = Fernet(key).encrypt(decrypted_access_token.encode())
        return f'{base64.b64encode(encrypted_access_token).decode("utf-8")}:{salt}'

    def load(self, full=False):
        path = Path(self.path)
        if not path.is_file():  # credentials file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

        # open the file with configparser
        credentials = configparser.ConfigParser()
        credentials.optionxform = str  # maintain key case
        credentials.read(self.path)
        credentials = json.loads(json.dumps(credentials._sections))  # TODO this is messy but works for now

        if full:
            return credentials
        return credentials.get(self.alias, None)

    def _get_token(self):
        # we should do a just-in-time decryption so unencrypted creds are not stored in memory
        return self.decrypt(self.credentials['accessToken'])

    def save(self, credentials: dict):
        full_credentials = self.load(full=True)
        if credentials is None:
            full_credentials.pop(self.alias, None)
        else:
            credentials['accessToken'] = self.encrypt(credentials['accessToken'])
            full_credentials[self.alias] = credentials
            # effectively a deep copy
            self.credentials = json.loads(json.dumps(credentials))

        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read_dict(full_credentials)

        # write the new credentials file
        with open(str(self.path), 'w') as f:
            config.write(f, space_around_delimiters=False)

    def delete(self):
        self.save(None)
