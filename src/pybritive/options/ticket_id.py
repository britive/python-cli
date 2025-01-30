import click

option = click.option(
    '--ticket-id',
    default=None,
    show_default=True,
    help='Ticket ID for the ITSM process, if a profile requires a ticket.',
)
