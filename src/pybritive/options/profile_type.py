import click

from pybritive.choices.profile_type import profile_type_choices

option = click.option(
    '--profile-type',
    type=profile_type_choices,
    show_choices=True,
    default=None,
    help='The profile type to use when checking out/in a profile.',
)
