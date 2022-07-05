import typer
from enums.mode import Mode

ModeOption = typer.Option(
    Mode.json, '-m', '--mode',
    help='The way in which the checked out credentials are presented. `integrate` will place the credentials into '
         'the cloud providers local credential file.'
)
