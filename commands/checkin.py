import click
from helpers.build_britive import build_britive
from options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='tenant,token')
@click.argument('profile')
def checkin(ctx, tenant, token, profile):
    """
    Checkin a profile.

    This command takes 1 required argument PROFILE. This should be a string representation of the profile
    that should be checked in. Format is "application name/environment name/profile name".
    """
    ctx.obj.britive.checkin(
        profile=profile
    )


