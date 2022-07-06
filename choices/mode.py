import click

mode_choices = click.Choice(
    [
        'text',
        'json',
        'env',
        'integrate',
        'env-nix',
        'env-wincmd',
        'env-winps',
        'awscredentialprocess'
    ],
    case_sensitive=False
)

