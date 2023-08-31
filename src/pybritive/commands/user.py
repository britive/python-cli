import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='tenant,token,silent,passphrase,federation_provider')
def user(ctx, tenant, token, silent, passphrase, federation_provider):
    """Print details about the authenticated identity."""
    ctx.obj.britive.user()
