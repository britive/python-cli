import click

from pybritive.helpers.build_britive import build_britive
from pybritive.options.britive_options import britive_options


@click.group()
def secret():
    """View or download a secret."""
    pass


@secret.command()
@build_britive
@britive_options(
    names='blocktime,justification,otp,maxpolltime,format,tenant,token,silent,passphrase,federation_provider'
)
@click.argument('path')
def view(
    ctx,
    blocktime,
    justification,
    otp,
    maxpolltime,
    output_format,
    tenant,
    token,
    silent,
    passphrase,
    federation_provider,
    path,
):
    """Display the secret value of the provided secret.

    This command takes 1 required argument `PATH`. This should be a string representation of the secret path.
    Ensure the leading `/` is provided.
    """
    if not path.startswith('/'):
        path = f'/{path}'

    ctx.obj.britive.viewsecret(
        path=path, blocktime=blocktime, justification=justification, otp=otp, maxpolltime=maxpolltime
    )


@secret.command()
@build_britive
@britive_options(
    names='file,blocktime,justification,otp,maxpolltime,format,silent,tenant,token,passphrase,federation_provider'
)
@click.argument('path')
def download(
    ctx,
    file,
    blocktime,
    justification,
    otp,
    maxpolltime,
    output_format,
    silent,
    tenant,
    token,
    passphrase,
    federation_provider,
    path,
):
    """Download the secret file.

    This command takes 1 required argument `PATH`. This should be a string representation of the secret path.
    Ensure the leading `/` is provided.
    """
    if not path.startswith('/'):
        path = f'/{path}'

    ctx.obj.britive.downloadsecret(
        path=path, blocktime=blocktime, justification=justification, otp=otp, maxpolltime=maxpolltime, file=file
    )
