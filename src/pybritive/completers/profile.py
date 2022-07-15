from ..helpers.cache import Cache
from ..helpers.config import ConfigManager


def profile_completer(ctx, param, incomplete):
    profiles = Cache().get_profiles()
    try:
        config = ConfigManager(None)
        config.load()
        aliases = config.profile_aliases
        alias_list = []
        if aliases:
            alias_list = list(aliases.keys())
    except Exception:
        alias_list = []

    options = profiles + alias_list

    return [o for o in options if incomplete.lower() in o.lower()]
