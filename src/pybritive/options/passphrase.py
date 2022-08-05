import click


option = click.option(
    '--passphrase', '-p',
    help='The passphrase to use for the encrypted-file credential backend type.',
    envvar='PYBRITIVE_ENCRYPTED_CREDENTIAL_PASSPHRASE',
    show_envvar=True,
    show_default=True
)

