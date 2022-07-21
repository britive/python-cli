import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options
from ..completers.profile import profile_completer


@click.command()
@build_britive
@britive_options(names='alias,blocktime,console,justification,mode,maxpolltime,silent,tenant,token,passphrase')
@click.argument('profile', shell_complete=profile_completer)
def checkout(ctx, alias, blocktime, console, justification, mode, maxpolltime, silent, tenant, token,
             passphrase, profile):
    """
    Checkout a profile.

    This command takes 1 required argument PROFILE. This should be a string representation of the profile
    that should be checked out. Format is "application name/environment name/profile name".
    """

    # silent will get passed in via @build_britive
    ctx.obj.britive.checkout(
        alias=alias,
        blocktime=blocktime,
        console=console,
        justification=justification,
        mode=mode,
        maxpolltime=maxpolltime,
        profile=profile
    )
