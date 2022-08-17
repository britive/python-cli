import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.command()
@build_britive
@britive_options(names='tenant,token,passphrase')
def login(ctx, tenant, token, passphrase):
    """Perform an interactive login to obtain temporary credentials.

    This only applies when an API token has not been specified via `--token,-T` or via environment variable
    `BRITIVE_API_TOKEN`.
    """
    ctx.obj.britive.login(explicit=True)
