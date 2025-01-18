import click

from pybritive.choices.browser import browser_choices

option = click.option(
    '--browser',
    type=browser_choices,
    default=None,
    show_choices=True,
    envvar='PYBRITIVE_BROWSER',
    show_envvar=True,
    help='The browser to use when opening a URL from the PyBritive CLI. Defaults to None which indicates the standard '
    'webbrowser selection process should be used. Can also source from PYBRITIVE_BROWSER.',
)
