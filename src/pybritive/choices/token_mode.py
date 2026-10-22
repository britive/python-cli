import click

# eval example: eval $(pybritive tokens create -m env)

# explanations:
#     clipboard: copy the access token to the clipboard
#     decode: decoded token header and claims (signature not verified) with issued/expires times
#     env: environment variable output (suitable for eval)
#     env-nix: environment variable output specifying "export"
#     env-wincmd: environment variable output specifying "set"
#     env-winps: environment variable output specifying "$env:"
#     json: accessToken and expiresOn, honoring --format (default)
#     token: the access token only

token_mode_choices = click.Choice(
    [
        'clipboard',
        'decode',
        'env',
        'env-nix',
        'env-wincmd',
        'env-winps',
        'json',
        'token',
    ],
    case_sensitive=False,
)
