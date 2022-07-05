import click
from choices.mode import mode_choices


option = click.option(
    '--mode', '-m',
    default='json',
    type=mode_choices,
    show_choices=True,
    show_default=True,
    help='The way in which the checked out credentials are presented. `integrate` will place the credentials into '
         'the cloud providers local credential file.'
)

