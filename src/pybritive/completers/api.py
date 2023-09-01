from britive.britive import Britive
from click.shell_completion import CompletionItem
import inspect


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

    existing = '.'.join(parts)

    options = []

    # vars happen at all levels
    for var, value in vars(b).items():
        # filter out things which should not show as completion items
        if not str(value).startswith('<britive.') or var == 'britive':
            continue

        method = f'{existing}.{var}' if not_base_level else var

        if method.lower().startswith(incomplete.lower()):
            doc_line = f'methods related to {var}'
            try:
                doc_line = inspect.getdoc(getattr(b, var)).split('\n')[0]
            except:
                pass
            options.append(CompletionItem(method, help=doc_line))

    # dir only happens at non "base" levels
    if not_base_level:
        # for each method in the class
        for func in dir(b):
            # filter out methods which are not callable and methods which are not "public"
            if not callable(getattr(b, func)) or func.startswith("_"):
                continue

            method = f'{existing}.{func}'

            # if this method is a potential match add it to the completion list
            if method.lower().startswith(incomplete.lower()):
                # grab the doc string if present
                doc_line = f'no docs found for {method}'

                try:
                    doc_line = inspect.getdoc(getattr(b, func)).split('\n')[0]
                except:
                    pass

                options.append(CompletionItem(method, help=doc_line))
    return options

