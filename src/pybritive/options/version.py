import click
import platform
import pkg_resources


# for --version we need to print the version and exit - nothing more, nothing less
def version_callback(ctx, self, value):
    if value:
        cli_version = pkg_resources.get_distribution('pybritive').version
        click.echo(f'pybritive: {cli_version} / platform: {platform.platform()} / python: {platform.python_version()}')
        raise click.exceptions.Exit()


option = click.option(
    '--version', '-v',
    default=None,
    callback=version_callback,
    is_eager=True,
    help='Prints the PyBritive CLI version and exits.',
    is_flag=True
)
