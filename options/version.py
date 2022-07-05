import click
import platform
from version import __version__


# for --version we need to print the version and exit - nothing more, nothing less
def version_callback(ctx, self, value):
    if value:
        cli_version = __version__
        click.echo(f'pybritve: {cli_version} / platform: {platform.platform()} / python: {platform.python_version()}')
        exit()


option = click.option(
    '--version', '-v',
    default=None,
    callback=version_callback,
    is_eager=True,
    help='Prints the PyBritive CLI version and exits.',
    is_flag=True
)
