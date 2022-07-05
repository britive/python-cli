import click
from choices.output_format import output_format_choices
from options.britive_options import britive_options
from helpers.config import ConfigManager


@click.group()
def configure():
    """
    Configures the PyBritive CLI.
    """


@configure.command()
@britive_options(names='configure_tenant,configure_alias,format,configure_prompt')
def tenant(tenant_name, alias, output_format, no_prompt):
    """
    Configures tenant level settings for the PyBritive CLI.

    If CLI options/flags are not provided an interactive data entry process will collect any needed data.
    """
    if not no_prompt:
        if not tenant_name:
            tenant_name = click.prompt(
                'The name of the tenant: [tenant].britive-app.com',
                type=str
            )
        if not alias:
            alias = click.prompt(
                'Optional alias for the above tenant. This alias would be used with the `--tenant` flag',
                default=tenant_name,
                type=str
            )
        if not output_format:
            output_format = click.prompt(
                'Output format (csv|json|table|yaml): ',
                default='json',
                type=output_format_choices
            )

    if not tenant_name  or len(tenant_name.strip()) == 0:
        click.echo('Tenant Name not provided.')
        exit()
    if not alias:
        alias = tenant_name
    if not output_format or output_format not in output_format_choices:
        click.echo(f'Invalid output format {output_format} provided. Defaulting to "json".')
        output_format = 'json'

    ConfigManager(save=True).save_tenant(
        tenant=tenant_name,
        alias=alias,
        output_format=output_format
    )


@configure.command(name='global')  # have to specify the name since global is a reserved word
@britive_options(names='configure_tenant,format,configure_prompt')
def global_command(default_tenant_name, output_format, no_prompt):
    """
    Configures global level settings for the PyBritive CLI.

    If CLI options/flags are not provided an interactive data entry process will collect any needed data.
    """
    if not no_prompt:
        if not default_tenant_name:
            default_tenant_name = click.prompt(
                'The default tenant name',
                type=str
            )
        if not output_format:
            output_format = click.prompt(
                'Output format (csv|json|table|yaml): ',
                default='json',
                type=output_format_choices
            )
        if not output_format or output_format not in output_format_choices:
            click.echo(f'Invalid output format {output_format} provided. Defaulting to "json".')
            output_format = 'json'

    ConfigManager(save=True).save_global(
        default_tenant_name=default_tenant_name,
        output_format=output_format
    )
