import click

option = click.option(
    '--federation-provider',
    '-P',
    help='Use a federation provider available in the Britive Python SDK for auto token creation. '
    'See CLI documentation at https://britive.github.io/python-cli/ for acceptable values.',
    default=None,
    show_default=True,
)
