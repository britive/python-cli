import click


option = click.option(
    '--query',
    default=None,
    help='JMESPath query to apply to the response.'
)
