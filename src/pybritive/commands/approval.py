import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.group()
def approval():
    """Manage approval requests"""
    pass


@approval.command()
@build_britive
@britive_options(names='blocktime,justification,maxpolltime,format,tenant,token,passphrase')
@click.argument('path')
def view(ctx, blocktime, justification, maxpolltime, output_format, tenant, token, passphrase, path):
    """Display the secret value of the provided secret.

    This command takes 1 required argument `PATH`. This should be a string representation of the secret path.
    Ensure the leading `/` is provided.
    """
    if not path.startswith('/'):
        path = f'/{path}'

    ctx.obj.britive.viewsecret(
        path=path,
        blocktime=blocktime,
        justification=justification,
        maxpolltime=maxpolltime
    )
