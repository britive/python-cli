import click

backend_choices = click.Choice(
    [
        'encrypted-file',
        'file',
    ],
    case_sensitive=False,
)
