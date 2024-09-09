import click

option = click.option(
    '--extend',
    '-e',
    default=False,
    is_flag=True,
    show_default=True,
    help='Extend the expiration time for a currently checked out profile.',
)
