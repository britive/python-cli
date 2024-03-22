import click


option = click.option(
    '--maxpolltime', '-x',
    default=600,
    show_default=True,
    help='Maximum seconds to poll before exiting.'
)
