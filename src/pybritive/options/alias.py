import click

option = click.option(
    '--alias', '-a',
    default=None,
    help='Alias for the profile so future checkouts can use the alias instead of the profile details.'
)
