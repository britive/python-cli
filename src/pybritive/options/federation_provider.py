import click

option = click.option(
    '--federation-provider', '-P',
    help='Use a federation provider available in the Britive Python SDK for auto token creation. '
         'Valid values are `aws[-profile]` and github[-audience]`. Optionally for the AWS provider a duration'
         'in seconds can be provided via `aws[-profile]_durationseconds` after which point the auto-generated'
         'credentials will expire.',
    default=None,
    show_default=True
)

