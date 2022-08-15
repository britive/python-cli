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

        if 'profiles' not in self.cache.keys():
            self.cache['profiles'] = []
        if 'awscredentialprocess' not in self.cache.keys():
            self.cache['awscredentialprocess'] = {}

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
        self.cache['profiles'] = []
        self.cache['awscredentialprocess'] = {}
        self.write()

    def get_awscredentialprocess(self, profile_name: str):
        try:
            ciphertext = self.cache['awscredentialprocess'].get(profile_name)
            if not ciphertext:
                return None
            return json.loads(self.string_encryptor.decrypt(ciphertext))
        except InvalidPassphraseException:  # if we cannot decrypt don't error - just make the API call to get the creds
            return None

    def save_awscredentialprocess(self, profile_name: str, credentials: dict):
        ciphertext = self.string_encryptor.encrypt(json.dumps(credentials, default=str))
        self.cache['awscredentialprocess'][profile_name] = ciphertext
        self.write()
