import click


option = click.option(
    '-T', '--token',
    default=None,
    help='API token.',
    envvar='BRITIVE_API_TOKEN',
    show_envvar=True,
    show_default=True
)
