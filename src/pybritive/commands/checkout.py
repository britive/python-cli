import click

from pybritive.helpers.build_britive import build_britive
from pybritive.helpers.profile_argument_decorator import click_smart_profile_argument
from pybritive.options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(
    names='alias,blocktime,console,justification,ticket_type,ticket_id,otp,mode,maxpolltime,silent,force_renew,aws_credentials_file,'
    'gcloud_key_file,verbose,extend,profile_type,tenant,token,passphrase,federation_provider'
)
@click_smart_profile_argument
def checkout(  # noqa: PLR0913
    ctx,
    alias,
    blocktime,
    console,
    justification,
    ticket_type,
    ticket_id,
    otp,
    mode,
    maxpolltime,
    silent,
    force_renew,
    aws_credentials_file,
    gcloud_key_file,
    verbose,
    extend,
    profile_type,
    tenant,
    token,
    passphrase,
    federation_provider,
    profile,
):
    """Checkout a profile.

    This command takes 1 required argument `PROFILE`. This should be a string representation of the profile
    that should be checked out. Format is `application name/environment name/profile name`.
    """

    # silent will get passed in via @build_britive
    ctx.obj.britive.checkout(
        alias=alias,
        blocktime=blocktime,
        console=console,
        justification=justification,
        ticket_type=ticket_type,
        ticket_id=ticket_id,
        otp=otp,
        mode=mode,
        maxpolltime=maxpolltime,
        profile=profile,
        passphrase=passphrase,
        force_renew=force_renew,
        aws_credentials_file=aws_credentials_file,
        gcloud_key_file=gcloud_key_file,
        verbose=verbose,
        extend=extend,
        profile_type=profile_type,
    )
