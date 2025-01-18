import click

from pybritive.choices.mode import mode_choices

# as of v1.1.0 not setting a default value here on purpose as the config file now has an
# aws section which provides a default value if the --mode option is omitted
# the default to `json` will occur now in helpers/cloud_credential_printer::CloudCredentialPrinter.__init__
option = click.option(
    '--mode',
    '-m',
    type=mode_choices,
    show_choices=True,
    help='The way in which the checked out credentials are presented. `integrate` will place the credentials into '
    'the cloud providers local credential file (AWS only). Value `env` can optionally include terminal specific '
    'options for setting environment variables '
    '(example: env-nix for Linux/Mac, env-wincmd for Windows Command Prompt, env-winps for Windows PowerShell).'
    '`gcloudauth` will save the generated key file/credentials to the pybritive config directory and generate a '
    'gcloud auth command which can be directly evaluated. Will default to `json` if not provided.',
)
