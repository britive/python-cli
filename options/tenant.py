import typer

TenantOption = typer.Option(
    None, '-t', '--tenant',
    help='Name of tenant.',
    envvar='BRITIVE_TENANT',
    show_envvar=True
)
