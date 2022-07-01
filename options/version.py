import typer
import platform


# for --version we need to print the version and exit - nothing more, nothing less
def version_callback(value: bool):
    if value:
        version = '0.1.0'  # TODO where to dynamically source this?
        typer.echo(f'pybritve: {version} / platform: {platform.platform()} / python: {platform.python_version()}')
        raise typer.Exit()


VersionOption = typer.Option(
    None, '-v', '--version',
    callback=version_callback,
    is_eager=True,
    help="List current version and exit."
)
