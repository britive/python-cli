import click

option = click.option(
    '--search-text',
    '-S',
    help='Filter list results to items matching the supplied search text.',
    default=None,
)
