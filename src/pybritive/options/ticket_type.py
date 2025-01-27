import click

option = click.option(
    '--ticket-type',
    default=None,
    show_default=True,
    help='Ticket type for the ITSM process, if a profile requires a ticket.',
)
