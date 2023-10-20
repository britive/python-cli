import click
from ..choices.ssh_key_source import ssh_key_source_choices


option = click.option(
    '--key-source', '-k',
    type=ssh_key_source_choices,
    show_choices=True,
    required=True,
    default='ssh-agent',
    show_default=True,
    help='The source of the SSH key used to authenticate to the remove server.'
)
