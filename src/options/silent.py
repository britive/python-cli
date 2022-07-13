import click


option = click.option(
    '--silent', '-s',
    default=False,
    is_flag=True,
    show_default=True,
    help='Enable silent mode.'
)

