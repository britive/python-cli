import click
from ..helpers.build_britive import build_britive


@click.group()
def clear():
    """Clear various local settings and configurations."""
    pass


@clear.command()
@build_britive
def cache(ctx):
    """Clears the local cache."""
    ctx.obj.britive.cache_clear()


@clear.command(name='gcloud-auth-key-files')
@build_britive
def gcloud_auth_key_files(ctx):
    """Clears the local gcloud auth key files."""
    ctx.obj.britive.clear_gcloud_auth_key_files()


