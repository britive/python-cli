import typer
from enums.output_format import OutputFormat
from options.output_format import OutputFormatOption
from options.configure_tenant import ConfigureTenantRequiredOption
from options.configure_alias import ConfigureTenantAlias
from options.configure_prompt import ConfigurePrompt
from config import ConfigManager

app = typer.Typer(add_completion=False)


@app.command()
def tenant(
        tenant_name: str = ConfigureTenantRequiredOption,
        alias: str = ConfigureTenantAlias,
        output_format: OutputFormat = OutputFormatOption,
        no_prompt: bool = ConfigurePrompt
):
    """
    Configures tenant level settings for the PyBritive CLI.

    If CLI options/flags are not provided an interactive data entry process will collect any needed data.
    """
    if not no_prompt:
        if not tenant_name:
            tenant_name = typer.prompt(
                'The name of the tenant: [tenant].britive-app.com',
                type=str
            )
        if not alias:
            alias = typer.prompt(
                'Optional alias for the above tenant. This alias would be used with the `--tenant` flag',
                default=tenant_name,
                type=str
            )
        if not output_format:
            output_format = typer.prompt(
                'Output format (csv|json|table|yaml): ',
                default='json',
                type=OutputFormat
            )

    if not tenant_name  or len(tenant_name.strip()) == 0:
        typer.echo('Tenant Name not provided.')
        typer.Abort()
    if not alias:
        alias = tenant_name
    if not output_format or output_format not in OutputFormat:
        typer.echo(f'Invalid output format {output_format} provided. Defaulting to "json".')
        output_format = 'json'

    ConfigManager(save=True).save_tenant(
        tenant=tenant_name,
        alias=alias,
        output_format=output_format.value
    )


@app.command(name='global')  # have to specify the name since global is a reserved word
def global_command(
        default_tenant_name: str = ConfigureTenantRequiredOption,
        output_format: OutputFormat = OutputFormatOption,
        no_prompt: bool = ConfigurePrompt
):
    """
    Configures global level settings for the PyBritive CLI.

    If CLI options/flags are not provided an interactive data entry process will collect any needed data.
    """
    if not no_prompt:
        if not default_tenant_name:
            default_tenant_name = typer.prompt(
                'The default tenant name',
                type=str
            )
        if not output_format:
            output_format = typer.prompt(
                'Output format (csv|json|table|yaml): ',
                default='json',
                type=OutputFormat
            )
        if not output_format or output_format not in OutputFormat:
            typer.echo(f'Invalid output format {output_format} provided. Defaulting to "json".')
            output_format = 'json'

    ConfigManager(save=True).save_global(
        default_tenant_name=default_tenant_name,
        output_format=output_format.value if output_format else None
    )


@app.callback()
def base():
    """
    Configures the PyBritive CLI.
    """


if __name__ == "__main__":
    app()
