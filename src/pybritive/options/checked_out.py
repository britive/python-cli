import click


option = click.option(
    '--checked-out', '-c',
    default=False,
    is_flag=True,
    show_default=True,
    help='Filter profile list to currently checked out profiles.'
)

