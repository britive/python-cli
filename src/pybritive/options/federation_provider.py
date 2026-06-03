import click

option = click.option(
    '--federation-provider',
    '-P',
    help='Use a federation provider available in the Britive Python SDK for auto token creation. '
    'Valid providers: aws, awsstsjwt, azuresmi, azureumi, bitbucket, gcp, github, gitlab, spacelift. '
    'For awsstsjwt use pipe-delimited params: awsstsjwt-<profile>|<audience>|<signing_algorithm>|<duration_seconds>. '
    'See CLI documentation at https://britive.github.io/python-cli/ for details.',
    default=None,
    show_default=True,
)
