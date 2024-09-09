import click

option = click.option(
    '--hostname',
    '-h',
    required=True,
    help='The SSH hostname from the SSH config file to which the ephemeral SSH public key will be pushed.',
)
