import click


option = click.option(
    '--console', '-c',
    default=False,
    is_flag=True,
    show_default=True,
    help='Checkout/checkin the console access for the profile instead of programmatic access.'
)
