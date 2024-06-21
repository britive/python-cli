import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options
from ..helpers.profile_argument_decorator import click_smart_profile_argument


@click.command()
@build_britive
@britive_options(names='alias,blocktime,console,justification,otp,mode,maxpolltime,silent,force_renew,aws_credentials_file,'
                       'gcloud_key_file,verbose,extend,profile_type,tenant,token,passphrase,federation_provider')
@click_smart_profile_argument
def checkout(ctx, alias, blocktime, console, justification, otp, mode, maxpolltime, silent, force_renew,
             aws_credentials_file, gcloud_key_file, verbose, extend, profile_type, tenant, token, passphrase,
             federation_provider, profile):
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
        profile_type=profile_type
    )
