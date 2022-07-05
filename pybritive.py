import click
from options.britive_options import britive_options
from commands.user import user as command_user
from commands.configure import configure as group_configure
from commands.login import login as command_login
from commands.logout import logout as command_logout
from commands.ls import ls as group_ls
from commands.checkout import checkout as command_checkout


# this is the "main" app - it really does nothing but print the overview/help section
@click.group()
@britive_options(names='version')
def cli(version):
    """
    PyBritive CLI - Pure Python Implementation for a Britive CLI
    """


cli.add_command(command_user)
cli.add_command(group_ls)
cli.add_command(command_login)
cli.add_command(command_logout)
cli.add_command(command_checkout)
cli.add_command(group_configure)


if __name__ == "__main__":
    cli()

