import click

option = click.option(
    '--tenant', '-t', 'configure_tenant', default=None, help='The name of the tenant: [tenant].britive-app.com.'
)
