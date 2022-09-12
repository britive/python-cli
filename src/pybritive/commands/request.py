import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options
from ..completers.profile import profile_completer

@click.group()
def request():
    """Provides functionality related to requesting approval to checkout a profile."""
    pass


@request.command()
@build_britive
@britive_options(names='justification,tenant,token,passphrase')
@click.argument('profile', shell_complete=profile_completer)
def submit(ctx, justification, tenant, token, passphrase, profile):
    """Submit a request to checkout a profile.

    Only applicable for profiles which require approval. This command will NOT block/wait until the request is
    approved or rejected. If you want to wait for the request to be approved, run the `checkout` command which will
    wait until the request is approved and then checkout the profile.

    This command takes 1 required argument `PROFILE`. This should be a string representation of the profile
    that should be checked out. Format is `application name/environment name/profile name`.
    """

    ctx.obj.britive.request_submit(
        profile=profile,
        justification=justification
    )


@request.command()
@build_britive
@britive_options(names='tenant,token,passphrase')
@click.argument('profile', shell_complete=profile_completer)
def withdraw(ctx, tenant, token, passphrase, profile):
    """Withdraw a request to checkout a profile.

    Only applicable for profiles which require approval.

    This command takes 1 required argument `PROFILE`. This should be a string representation of the profile
    that should be checked out. Format is `application name/environment name/profile name`.
    """

    ctx.obj.britive.request_withdraw(
        profile=profile
    )