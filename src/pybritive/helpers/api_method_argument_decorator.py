import click


def click_smart_api_method_argument(func):
    from pybritive.completers.api import api_completer
    dec = click.argument('method', shell_complete=api_completer)
    return dec(func)
