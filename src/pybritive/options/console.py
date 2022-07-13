import click


option = click.option(
    '--console', '-c',
    default=False,
    is_flag=True,
    show_default=True,
    help='Checkout the console access for the profile instead of programmatic access.'
)

