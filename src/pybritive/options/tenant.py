import click


option = click.option(
    '-t', '--tenant',
    default=None,
    help='Name of tenant.',
    envvar='BRITIVE_TENANT',
    show_envvar=True,
    show_default=True
)
