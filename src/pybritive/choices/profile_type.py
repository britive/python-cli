import click

# eval example: eval $(pybritive checkout test -m env)

profile_type_choices = click.Choice(
    [
        'my-access',
        'my-resources'
    ],
    case_sensitive=False
)
