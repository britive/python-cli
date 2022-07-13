import click


option = click.option(
    '--justification', '-j',
    default=None,
    show_default=True,
    help='Justification for the checkout approval process, if the profile checkout requires approval.'
)

