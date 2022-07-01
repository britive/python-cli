import typer


TokenOption = typer.Option(
    None, '-T', '--token',
    help='API token.',
    envvar='BRITIVE_API_TOKEN',
    show_envvar=True
)
