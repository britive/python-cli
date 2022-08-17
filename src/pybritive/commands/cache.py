import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.group()
def cache():
    """Manage local cache settings."""
    pass


@cache.command()
@build_britive
@britive_options(names='tenant,token,passphrase')
def profiles(ctx, tenant, token, passphrase):
    """Cache profiles locally to facilitate auto-completion of profile names on checkin/checkout."""
    ctx.obj.britive.cache_profiles()


@cache.command()
@build_britive
def clear(ctx):
    """Clears the local cache."""
    ctx.obj.britive.cache_clear()



