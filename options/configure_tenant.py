import typer


def validate_tenant(value: str):
    if value is None:
        return None
    return value.replace('.britive-app.com', '')  # just in case


ConfigureTenantRequiredOption = typer.Option(
    None, '-t', '--tenant',
    callback=validate_tenant,
    help='The name of the tenant: [tenant].britive-app.com.'
)
