import click

option = click.option(
    '--justification',
    '-j',
    default=None,
    show_default=True,
    help='Justification for the approval process, if a profile checkout or secret access requires approval.',
)
