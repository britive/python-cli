import click

from pybritive.choices.token_mode import token_mode_choices

option = click.option(
    '--mode',
    '-m',
    type=token_mode_choices,
    show_choices=True,
    help='Print BRITIVE_TENANT, BRITIVE_TOKEN and BRITIVE_TOKEN_EXPIRATION as environment variables (suitable for '
    'eval) instead of the --format output. Value `env` can optionally include terminal specific options '
    '(example: env-nix for Linux/Mac, env-wincmd for Windows Command Prompt, env-winps for Windows PowerShell).',
)
