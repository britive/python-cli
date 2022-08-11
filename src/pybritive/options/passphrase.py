import click


option = click.option(
    '--passphrase', '-p',
    help='The passphrase to use for encrypting credentials.',
    envvar='PYBRITIVE_ENCRYPTED_CREDENTIAL_PASSPHRASE',
    show_envvar=True,
    show_default=True
)

