import typer

ModeOption = typer.Option(
    None, '-m', '--mode',
    help='The way in which the checked out credentials are presented. `integrate` will place the credentials into '
         'the cloud providers local credentials file.'
)
