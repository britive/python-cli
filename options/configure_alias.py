import typer

ConfigureTenantAlias = typer.Option(
    None, '-a', '--alias',
    help='Optional alias for the above tenant. This alias would be used with the `--tenant` flag.'
)
