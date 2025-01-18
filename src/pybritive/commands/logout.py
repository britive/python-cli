import click

from pybritive.helpers.build_britive import build_britive
from pybritive.options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='tenant,silent,passphrase')
def logout(ctx, tenant, silent, passphrase):
    """Logout of an interactive login session.

    This only applies when an API token has not been specified via `--token,-T` or via environment variable
    `BRITIVE_API_TOKEN`.
    """
    ctx.obj.britive.logout()
