import click

option = click.option(
    '--otp',
    '-o',
    default=None,
    show_default=False,
    help='OTP to checkout a profile, download a secret, or view a secret, if MFA is required.',
)
