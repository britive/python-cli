import click


option = click.option(
    '--aws-credentials-file',
    default=None,
    help='AWS Programmatic Only - When mode is `integrate` specify a non-default location for the AWS '
         'credentials file.',
    envvar='AWS_SHARED_CREDENTIALS_FILE',
    show_envvar=True,
    show_default=True
)
