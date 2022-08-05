import click


option = click.option(
    '--maxpolltime', '-p',
    default=600,
    show_default=True,
    help='Maximum seconds to poll before exiting.'
)

