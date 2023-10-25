import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.group()
def cache():
    """Manage local cache settings."""
    pass


@cache.command()
@build_britive
@britive_options(names='tenant,token,silent,passphrase,federation_provider')
def profiles(ctx, tenant, token, silent, passphrase, federation_provider):
    """Cache profiles locally to facilitate auto-completion of profile names on checkin/checkout."""
    ctx.obj.britive.cache_profiles(from_cache_command=True)


@cache.command()
@build_britive
@britive_options(names='tenant,token,silent,passphrase,federation_provider')
def kubeconfig(ctx, tenant, token, silent, passphrase, federation_provider):
    """Cache a Britive managed kube config file based on the profiles to which the caller has access."""
    ctx.obj.britive.construct_kube_config(from_cache_command=True)


@cache.command()
@build_britive
def clear(ctx):
    """Clears the local cache."""
    ctx.obj.britive.cache_clear()
