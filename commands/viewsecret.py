import click
from helpers.build_britive import build_britive
from options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='blocktime,justification,maxpolltime,format,tenant,token')
@click.argument('path')
def viewsecret(ctx, blocktime, justification, maxpolltime, output_format, tenant, token, path):
    """
    Display the secret value of the provided secret.

    This command takes 1 required argument PATH. This should be a string representation of the secret path.
    Ensure the leading / is provided.
    """
    if not path.startswith('/'):
        path = f'/{path}'

    ctx.obj.britive.viewsecret(
        path=path,
        blocktime=blocktime,
        justification=justification,
        maxpolltime=maxpolltime
    )
