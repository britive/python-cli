import click
from helpers.build_britive import build_britive
from options.britive_options import britive_options


@click.group()
def ls():
    """
    List resources available for currently authenticated identity.
    """
    pass


@ls.command()
@build_britive
@britive_options(names='tenant,token,format')
def applications(ctx, tenant, token, output_format):
    """List applications for the currently authenticated identity."""
    ctx.obj.britive.list_applications()


@ls.command()
@build_britive
@britive_options(names='tenant,token,format')
def environments(ctx, tenant, token, output_format):
    """List environments for the currently authenticated identity."""
    ctx.obj.britive.list_environments()


@ls.command()
@build_britive
@britive_options(names='tenant,token,format')
def profiles(ctx, tenant, token, output_format):
    """List profiles for the currently authenticated identity."""
    ctx.obj.britive.list_profiles()


@ls.command()
@build_britive
@britive_options(names='tenant,token,format')
def secrets(ctx, tenant, token, output_format):
    """List secrets for the currently authenticated identity."""
    ctx.obj.britive.list_secrets()



