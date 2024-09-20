import click

ssh_key_source_choices = click.Choice(
    [
        'ssh-agent',  # use the ssh-agent and ssh-add the key so the IdentityFile parameter can be omitted
        'static',  # use a well known key name format so IdentityFile parameter can be used
    ],
    case_sensitive=False,
)
