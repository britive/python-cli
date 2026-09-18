import click

from pybritive.helpers.build_britive import build_britive
from pybritive.options.britive_options import britive_options


@click.group()
def tokens():
    """Manage temporary tokens for your authenticated identity."""


@tokens.command()
@build_britive
@britive_options(names='format,tenant,token,silent,passphrase,federation_provider')
@click.option(
    '--duration-seconds',
    type=click.IntRange(1, 86400),
    default=None,
    help='Requested lifetime in seconds. Omit to use the tenant default. The tenant maximum also applies.',
)
def create(ctx, output_format, tenant, token, silent, passphrase, federation_provider, duration_seconds):
    """Create a temporary bearer token for your authenticated identity.

    Requires securityadmin.temptoken.create. A temporary token cannot create another temporary token.
    Prints accessToken and expiresOn, including when --silent is set. The token is returned only once
    and is not saved as your CLI login credential.
    """
    ctx.obj.britive.create_temp_token(duration_seconds=duration_seconds)


@tokens.command()
@build_britive
@britive_options(names='format,tenant,token,silent,passphrase,federation_provider')
def list(ctx, output_format, tenant, token, silent, passphrase, federation_provider):
    """List temporary tokens (not yet implemented)."""
    # Remove this guard when the SDK implements the operation.
    raise click.ClickException('Listing temporary tokens is not yet implemented.')
    ctx.obj.britive.list_temp_tokens()


@tokens.command()
@build_britive
@britive_options(names='format,tenant,token,silent,passphrase,federation_provider')
@click.argument('token_id')
def get(ctx, output_format, tenant, token, silent, passphrase, federation_provider, token_id):
    """View a temporary token (not yet implemented).

    TOKEN_ID is provisional, pending the API contract.
    """
    # Remove this guard when the SDK implements the operation.
    raise click.ClickException('Viewing temporary tokens is not yet implemented.')
    ctx.obj.britive.get_temp_token(token_id=token_id)


@tokens.command()
@build_britive
@britive_options(names='tenant,token,silent,passphrase,federation_provider')
@click.argument('token_id')
def revoke(ctx, tenant, token, silent, passphrase, federation_provider, token_id):
    """Revoke a temporary token (not yet implemented).

    TOKEN_ID is provisional, pending the API contract.
    """
    # Remove this guard when the SDK implements the operation.
    raise click.ClickException('Revoking temporary tokens is not yet implemented.')
    ctx.obj.britive.revoke_temp_token(token_id=token_id)
