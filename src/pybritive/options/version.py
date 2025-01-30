import platform
from importlib.metadata import version

import click


# for --version we need to print the version and exit - nothing more, nothing less
def version_callback(ctx, self, value):
    if value:
        cli_version = version('pybritive')
        click.echo(f'pybritive: {cli_version} / platform: {platform.platform()} / python: {platform.python_version()}')
        raise click.exceptions.Exit


option = click.option(
    '--version',
    '-v',
    default=None,
    callback=version_callback,
    is_eager=True,
    help='Prints the PyBritive CLI version and exits.',
    is_flag=True,
)
