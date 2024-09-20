import os
import sys

import click

from .commands.api import api as command_api
from .commands.aws import aws as group_aws
from .commands.cache import cache as group_cache
from .commands.checkin import checkin as command_checkin
from .commands.checkout import checkout as command_checkout
from .commands.clear import clear as group_clear
from .commands.configure import configure as group_configure
from .commands.login import login as command_login
from .commands.logout import logout as command_logout
from .commands.ls import ls as group_ls
from .commands.request import request as group_request
from .commands.secret import secret as group_secret
from .commands.ssh import ssh as group_ssh
from .commands.user import user as command_user
from .options.britive_options import britive_options


def safe_cli():
    debug = os.getenv('PYBRITIVE_DEBUG')
    try:
        if not debug:
            sys.tracebacklimit = 0
        cli()
    except Exception as e:
        if debug:
            raise e
        raise e from None


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
cli.add_command(command_checkin)
cli.add_command(group_secret)
cli.add_command(group_cache)
cli.add_command(group_request)
cli.add_command(group_clear)
cli.add_command(command_api)
cli.add_command(group_ssh)
cli.add_command(group_aws)


if __name__ == '__main__':
    safe_cli()
