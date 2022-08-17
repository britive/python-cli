import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='tenant,token,passphrase')
def user(ctx, tenant, token, passphrase):
    """Print details about the authenticated identity."""
    ctx.obj.britive.user()

