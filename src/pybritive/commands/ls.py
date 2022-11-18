import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.group()
def ls():
    """List resources available for currently authenticated identity."""
    pass


@ls.command()
@build_britive
@britive_options(names='format,tenant,token,passphrase,federation_provider')
def applications(ctx, output_format, tenant, token, passphrase, federation_provider):
    """List applications for the currently authenticated identity."""
    ctx.obj.britive.list_applications()


@ls.command()
@build_britive
@britive_options(names='format,tenant,token,passphrase,federation_provider')
def environments(ctx, output_format, tenant, token, passphrase, federation_provider):
    """List environments for the currently authenticated identity."""
    ctx.obj.britive.list_environments()


@ls.command()
@build_britive
@britive_options(names='checked_out,output_format,tenant,token,passphrase,federation_provider')
def profiles(ctx, checked_out, output_format, tenant, token, passphrase, federation_provider):
    """List profiles for the currently authenticated identity."""
    ctx.obj.britive.list_profiles(checked_out=checked_out)


@ls.command()
@build_britive
@britive_options(names='format,tenant,token,passphrase, federation_provider')
def secrets(ctx, output_format, tenant, token, passphrase, federation_provider):
    """List secrets for the currently authenticated identity."""
    ctx.obj.britive.list_secrets()



