import click


def validate_tenant(ctx, self, value):
    if value is None:
        return None
    return value.replace('.britive-app.com', '')  # just in case


option = click.option(
    '--tenant', '-t', 'configure_tenant',
    callback=validate_tenant,
    default=None,
    help='The name of the tenant: [tenant].britive-app.com.'
)
