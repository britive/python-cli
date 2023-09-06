from pathlib import Path
import json
import os
from .encryption import StringEncryption, InvalidPassphraseException


class Cache:
    def __init__(self, passphrase: str = None):
        self.passphrase = passphrase
        self.string_encryptor = StringEncryption(passphrase=self.passphrase)
        home = os.getenv('PYBRITIVE_HOME_DIR', str(Path.home()))
        self.path = str(Path(home) / '.britive' / 'pybritive.cache')  # handle os specific separators properly
        self.cache = {}
        self.default_key_values = {
            'profiles': [],
            'awscredentialprocess': {},
            'kube-exec': {}
        }
        self.load()

    def load(self):
        path = Path(self.path)
        if not path.is_file():  # cache file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            cache = {
                'profiles': []
            }
            path.write_text(json.dumps(cache, indent=2, default=str))

        with open(str(self.path), 'r') as f:
            try:
                self.cache = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self.cache = {}

        self.cache = {**self.default_key_values, **self.cache}

    def write(self):
        # write the new cache file
        with open(str(self.path), 'w') as f:
            f.write(json.dumps(self.cache, indent=2, default=str))

    def get_profiles(self):
        return self.cache.get('profiles', [])

    def save_profiles(self, profiles: list):
        self.cache['profiles'] += profiles
        # dedup the list of profiles
        self.cache['profiles'] = list(dict.fromkeys(self.cache['profiles']))
        self.write()

    def clear(self):
        self.cache = self.default_key_values
        self.write()

    def get_credentials(self, profile_name: str, mode: str = 'awscredentialprocess'):
        try:
            ciphertext = self.cache[mode].get(profile_name.lower())
            if not ciphertext:
                return None
            return json.loads(self.string_encryptor.decrypt(ciphertext))
        except InvalidPassphraseException:  # if we cannot decrypt don't error - just make the API call to get the creds
            return None

    def save_credentials(self, profile_name: str, credentials: dict, mode: str = 'awscredentialprocess'):
        ciphertext = self.string_encryptor.encrypt(json.dumps(credentials, default=str))
        self.cache[mode][profile_name.lower()] = ciphertext
        self.write()

    def clear_credentials(self, profile_name: str, mode: str = 'awscredentialprocess'):
        self.cache[mode].pop(profile_name.lower(), None)
        self.write()
