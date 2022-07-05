import click

mode_choices = click.Choice(
    [
        'text',
        'json',
        'env',
        'integrate'
    ],
    case_sensitive=False
)

