import click

from pybritive.helpers.build_britive import build_britive
from pybritive.options.britive_options import britive_options


@click.group()
def ls():
    """List resources available for currently authenticated identity."""
    pass


@ls.command()
@build_britive
@britive_options(names='search_text,format,tenant,token,silent,passphrase,federation_provider')
def applications(ctx, search_text, output_format, tenant, token, silent, passphrase, federation_provider):
    """List applications for the currently authenticated identity."""
    ctx.obj.britive.list_applications(search_text=search_text)


@ls.command()
@build_britive
@britive_options(names='format,tenant,token,silent,passphrase,federation_provider')
def approvals(ctx, output_format, tenant, token, silent, passphrase, federation_provider):
    """List approvals for the currently authenticated identity."""
    ctx.obj.britive.list_approvals()


@ls.command()
@build_britive
@britive_options(names='search_text,format,tenant,token,silent,passphrase,federation_provider')
def environments(ctx, search_text, output_format, tenant, token, silent, passphrase, federation_provider):
    """List environments for the currently authenticated identity."""
    ctx.obj.britive.list_environments(search_text=search_text)


@ls.command()
@build_britive
@britive_options(
    names='checked_out,profile_type,search_text,output_format,tenant,token,silent,passphrase,federation_provider'
)
def profiles(
    ctx,
    checked_out,
    profile_type,
    search_text,
    output_format,
    tenant,
    token,
    silent,
    passphrase,
    federation_provider,
):
    """List profiles for the currently authenticated identity."""
    ctx.obj.britive.list_profiles(checked_out=checked_out, profile_type=profile_type, search_text=search_text)


@ls.command()
@build_britive
@britive_options(names='format,tenant,token,silent,passphrase,federation_provider')
def requests(ctx, output_format, tenant, token, silent, passphrase, federation_provider):
    """List requests for the currently authenticated identity."""
    ctx.obj.britive.list_requests()


@ls.command()
@build_britive
@britive_options(names='search_text,format,tenant,token,silent,passphrase,federation_provider')
def resources(ctx, search_text, output_format, tenant, token, silent, passphrase, federation_provider):
    """List resources for the currently authenticated identity."""
    ctx.obj.britive.list_resources(search_text=search_text)


@ls.command()
@build_britive
@britive_options(names='search_text,format,tenant,token,silent,passphrase,federation_provider')
def secrets(ctx, search_text, output_format, tenant, token, silent, passphrase, federation_provider):
    """List secrets for the currently authenticated identity."""
    ctx.obj.britive.list_secrets(search_text=search_text)
