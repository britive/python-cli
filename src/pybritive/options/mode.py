import click
from ..choices.mode import mode_choices


option = click.option(
    '--mode', '-m',
    default='json',
    type=mode_choices,
    show_choices=True,
    show_default=True,
    help='The way in which the checked out credentials are presented. `integrate` will place the credentials into '
         'the cloud providers local credential file (AWS only). Value `env` can optionally include terminal specific '
         'options for setting environment variables '
         '(example: env-nix for Linux/Mac, env-wincmd for Windows Command Prompt, env-winps for Windows PowerShell).'
)

