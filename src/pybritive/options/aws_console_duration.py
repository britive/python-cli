import click

option = click.option(
    '--duration', '-d',
    default=12 * 60 * 60,  # 12 hours in seconds (43200)
    show_default=True,
    help='Number of seconds the console session should last. Minimum of 900 and maximum of 43200 (the default).'
)
