import click
from ..choices.backend import backend_choices

option = click.option(
    '--backend', '-b', 'configure_backend',
    default=None,
    type=backend_choices,
    show_choices=True,
    show_default=True,
    help='The backend used to store temporary access tokens to authenticate against the Britive tenant.'
)
