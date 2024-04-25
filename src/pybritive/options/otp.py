import click


option = click.option(
    '--otp', '-o',
    default=None,
    show_default=False,
    help='OTP to checkout a profile, if the profile checkout requires MFA.',
)
