import hashlib
import json
import os
from pathlib import Path
import time
from .encryption import StringEncryption, InvalidPassphraseException


class Cache:
    def __init__(self, passphrase: str = None):
        self.passphrase = passphrase
        self.string_encryptor = StringEncryption(passphrase=self.passphrase)
        home = os.getenv('PYBRITIVE_HOME_DIR', str(Path.home()))
        self.base_path = str(Path(home) / '.britive')
        self.path = str(Path(self.base_path) / 'pybritive.cache')  # handle os specific separators properly
        self.cache = {}
        self.default_key_values = {
            'profiles': [],
            'awscredentialprocess': {},
            'kube-exec': {},
            'banners': {}
        }
        self.load()

    def load(self):
        path = Path(self.path)
        if not path.is_file():  # cache file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            cache = {
                'profiles': []
            }
            path.write_text(json.dumps(cache, indent=2, default=str), encoding='utf-8')

        with open(str(self.path), 'r', encoding='utf-8') as f:
            try:
                self.cache = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self.cache = {}

        self.cache = {**self.default_key_values, **self.cache}

    def write(self):
        # write the new cache file
        with open(str(self.path), 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.cache, indent=2, default=str))

    def get_profiles(self):
        return self.cache.get('profiles', [])

    def save_profiles(self, profiles: list):
        self.cache['profiles'] += profiles
        # dedup the list of profiles
        self.cache['profiles'] = list(dict.fromkeys(self.cache['profiles']))
        self.write()

    def clear(self):
        # write empty cache file
        self.cache = self.default_key_values
        self.write()

    def clear_kubeconfig(self):
        # delete kube config if it exists
        kubeconfig = Path(self.base_path) / 'kube' / 'config'
        # kubeconfig.unlink(missing_ok=True)
        # removed for now, for 3.7 compatability
        try:
            kubeconfig.unlink()
        except FileNotFoundError:
            pass

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

    @staticmethod
    def hash_banner(banner: dict) -> str:
        return hashlib.sha512(json.dumps(banner, default=str)).hexdigest()

    def banner_expired(self, tenant: str) -> bool:
        cached_banner_data = self.cache.get('banners', {}).get(tenant)
        expires = 0
        if cached_banner_data is not None:
            expires = cached_banner_data.get('expires', 0)
        return expires < int(time.time())

    def save_banner(self, tenant: str, banner: dict) -> bool:
        # if someone called this then we simply save the banner
        # regardless of whether the cached record has expired yet
        # as we assume the caller knows what they are doing

        cached_banner_data = self.cache.get('banners', {}).get(tenant, {})
        cached_hash = cached_banner_data.get('hash', '')
        new_hash = hashlib.sha512(json.dumps(banner, default=str, sort_keys=True).encode('utf-8')).hexdigest()
        self.cache['banners'][tenant] = {
            'hash': new_hash,
            'expires': int(time.time()) + (5 * 60)
        }
        self.write()

        # return True if the hashes have changed, False is they are equal
        return cached_hash != new_hash
