import click

option = click.option(
    '--blocktime', '-b',
    default=3,
    show_default=True,
    help='Seconds to wait before starting to poll for credentials. If not provided will default to 60 for profiles '
         'that require approval and 3 for profiles without approval.'
)

