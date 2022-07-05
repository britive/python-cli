import typer


MaxPollTimeOption = typer.Option(
    600, '-p', '--maxpolltime',
    help='Maximum seconds to poll before exiting.'
)
