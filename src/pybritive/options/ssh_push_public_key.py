import click


option = click.option(
    '--push-public-key', '-P',
    required=True,
    default=False,
    is_flag=True,
    help='Whether to push a public key to the EC2 instance via EC2 Instance Connect'
)
