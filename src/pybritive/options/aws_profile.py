import click

option = click.option(
    '--profile',
    '-p',
    default=None,
    help='AWS CLI profile from which credentials will be sourced. Defaults to None which indicates that the default '
    'credential provider chain should be used.',
    show_envvar=True,
    show_default=True,
)
