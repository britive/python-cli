import click

from pybritive.completers.tenant import tenant_completer

option = click.option(
    '-t',
    '--tenant',
    default=None,
    help='Name of tenant.',
    envvar='BRITIVE_TENANT',
    show_envvar=True,
    show_default=True,
    shell_complete=tenant_completer,
)
