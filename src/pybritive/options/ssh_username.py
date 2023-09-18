import click


option = click.option(
    '--username', '-u',
    required=True,
    help='The EC2 OS username for whom the ephemeral SSH public key will be pushed.'
)
