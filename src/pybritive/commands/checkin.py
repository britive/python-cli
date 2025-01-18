import click

from pybritive.helpers.build_britive import build_britive
from pybritive.helpers.profile_argument_decorator import click_smart_profile_argument
from pybritive.options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='console,profile_type,tenant,token,silent,passphrase,federation_provider')
@click_smart_profile_argument
def checkin(ctx, console, profile_type, tenant, token, silent, passphrase, federation_provider, profile):
    """Checkin a profile.

    This command takes 1 required argument `PROFILE`. This should be a string representation of the profile
    that should be checked in. Format is `application name/environment name/profile name`.
    """
    ctx.obj.britive.checkin(profile=profile, console=console, profile_type=profile_type)
