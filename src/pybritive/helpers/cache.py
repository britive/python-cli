from pathlib import Path
import configparser
import json


class Cache:
    def __init__(self):
        self.path = str(Path.home() / '.britive' / 'pybritive.cache')  # handle os specific separators properly
        self.cache = {}
        self.profiles = []
        self.load()

    def load(self):
        path = Path(self.path)
        if not path.is_file():  # cache file does not yet exist, create it as an empty file
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_text('')

        cache = configparser.ConfigParser()
        cache.optionxform = str  # maintain key case
        cache.read(str(self.path))
        cache = json.loads(json.dumps(cache._sections))  # TODO this is messy but works for now
        self.cache = cache
        self.profiles = list(self.cache.get('profiles', {}).keys())

    def write(self):
        cache = {
            'profiles': {}
        }
        profiles_dict = {}
        for p in self.profiles:
            profiles_dict[p] = ''
        self.cache['profiles'] = profiles_dict

        config = configparser.ConfigParser()
        config.optionxform = str  # maintain key case
        config.read_dict(self.cache)

        # write the new cache file
        with open(str(self.path), 'w') as f:
            config.write(f, space_around_delimiters=False)

    def get_profiles(self):
        return self.profiles

    def save_profiles(self, profiles: list):
        self.profiles += profiles
        self.write()

    def clear(self):
        self.profiles = []
        self.write()
