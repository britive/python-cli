import click

option = click.option(
    '--port-number', '-p', required=True, help='The SSH port number from the SSH config file for the given host.'
)
