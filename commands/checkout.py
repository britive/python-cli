import click
from helpers.build_britive import build_britive
from options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='alias,mode,blocktime,maxpolltime,tenant,token')
@click.argument('profile')
def checkout(ctx, alias, mode, blocktime, maxpolltime, tenant, token, profile):
    """
    Checkout a profile.

    This command takes 1 required argument PROFILE. This should be a string representation of the profile
    that should be checked out. Format is "application name/environment name/profile name".
    """
    pass

