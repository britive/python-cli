import click


option = click.option(
    '--alias', '-a', 'configure_alias',
    default=None,
    help='Optional alias for the above tenant. This alias would be used with the `--tenant` flag.'
)

