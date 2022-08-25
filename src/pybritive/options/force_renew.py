import click

option = click.option(
    '--force-renew',
    default=None,
    show_default=True,
    type=int,
    help='AWS Programmatic Only - If the credentials are to expire within the specified number of minutes, check in '
         'the profile first and check it out again to get a new set of credentials.'
)

