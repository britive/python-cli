from pathlib import Path
import json
import os


class Cache:
    def __init__(self):
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

    def write(self):
        # write the new cache file
        with open(str(self.path), 'w') as f:
            f.write(json.dumps(self.cache, indent=2, default=str))

    def get_profiles(self):
        return self.cache.get('profiles', [])

    def save_profiles(self, profiles: list):
        self.cache['profiles'] += profiles
        self.write()

    def clear(self):
        self.cache['profiles'] = []
        self.write()
