import typer

AliasOption = typer.Option(
    None, '-a', '--alias',
    help='Alias for the profile so future checkouts can use the alias instead of the profile details.'
)
