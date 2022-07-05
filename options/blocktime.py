import typer


BlockTimeOption = typer.Option(
    3, '-b', '--blocktime',
    help='Seconds to wait before starting to poll for credentials. If not provided will default to 60 for profiles '
         'that require approval and 3 for profiles without approval.'
)
