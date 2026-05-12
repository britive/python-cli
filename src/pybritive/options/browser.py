import click

from pybritive.choices.browser import browser_choices

option = click.option(
    '--browser',
    type=browser_choices,
    default=None,
    show_choices=True,
    envvar='PYBRITIVE_BROWSER',
    show_envvar=True,
    help='The browser to use when opening URLs. Accepts a predefined name (chrome, chromium, firefox, macosx, '
    'mozilla, safari, windows-default) or a custom command with %s as the URL placeholder '
    '(e.g. "firefox %s", "chromium-browser %s"). '
    'Defaults to the OS default browser. Can also source from PYBRITIVE_BROWSER.',
)
