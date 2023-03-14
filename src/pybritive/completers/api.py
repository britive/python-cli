from britive.britive import Britive
import json


def api_completer(ctx, param, incomplete):
    # create an instance of the Britive class, so we can inspect it
    # this doesn't need to actually connect to any tenant, and we couldn't even if we
    # wanted to since when performing shell completion we have no tenant/token
    # context in order to properly establish a connection.
    b = Britive(token='ignore', tenant='britive.com', query_features=False)

    # parse the incomplete command, so we can determine where in the "hierarchy" we are
    # and what commands/subcommands the user should be presented with
    parts = incomplete.split('.')[:-1]
    not_base_level = len(parts) > 0
    for part in parts:
        b = getattr(b, part)

    options = []

    # vars happen at all levels
    options += [var for var, value in vars(b).items() if str(value).startswith('<britive.') and var != 'britive']

    # dir only happens at non "base" levels
    if not_base_level:
        options += [func for func in dir(b) if callable(getattr(b, func)) and not func.startswith("_")]

    # pull it all back together and make it look nice
    existing = '.'.join(parts)
    options = [f'{existing}.{o}' if not_base_level else o for o in options]

    return [o for o in options if o.lower().startswith(incomplete.lower())]
