import click


backend_choices = click.Choice(
    [
        'file',
        'encrypted-file'
    ],
    case_sensitive=False
)

