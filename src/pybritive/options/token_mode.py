import click

from pybritive.choices.token_mode import token_mode_choices

option = click.option(
    '--mode',
    '-m',
    type=token_mode_choices,
    show_choices=True,
    help='The way in which the temporary token is presented. `token` prints only the access token. `decode` prints '
    'the token header and claims (signature not verified) with issued/expires times. Value `env` prints '
    'BRITIVE_TENANT, BRITIVE_TOKEN and BRITIVE_TOKEN_EXPIRATION for eval and can optionally include terminal '
    'specific options for setting environment variables '
    '(example: env-nix for Linux/Mac, env-wincmd for Windows Command Prompt, env-winps for Windows PowerShell). '
    'Will default to `json` if not provided.',
)
