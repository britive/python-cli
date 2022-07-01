from typing import Optional
import typer
from helpers.inject_common_options import inject_common_options
from enums.output_format import OutputFormat
from options.output_format import OutputFormatOption
from options.token import TokenOption

app = typer.Typer(add_completion=False)


@app.command()
@inject_common_options
def applications(
        ctx: typer.Context,
        output_format: Optional[OutputFormat] = OutputFormatOption,
        token: Optional[str] = TokenOption  # used by @inject common_options
):
    """List applications for the currently authenticated identity."""
    ctx.obj.britive.set_output_format(None if output_format is None else output_format.value)
    ctx.obj.britive.list_applications()


@app.command()
@inject_common_options
def environments(
        ctx: typer.Context,
        output_format: Optional[OutputFormat] = OutputFormatOption,
        token: Optional[str] = TokenOption  # used by @inject common_options
):
    """List environments for the currently authenticated identity."""
    ctx.obj.britive.set_output_format(None if output_format is None else output_format.value)
    ctx.obj.britive.list_environments()


@app.command()
@inject_common_options
def profiles(
        ctx: typer.Context,
        output_format: Optional[OutputFormat] = OutputFormatOption,
        token: Optional[str] = TokenOption  # used by @inject common_options
):
    """List profiles for the currently authenticated identity."""
    ctx.obj.britive.set_output_format(None if output_format is None else output_format.value)
    ctx.obj.britive.list_profiless()


@app.command()
@inject_common_options
def secrets(
        ctx: typer.Context,
        output_format: Optional[OutputFormat] = OutputFormatOption,
        token: Optional[str] = TokenOption  # used by @inject common_options
):
    """List secrets for the currently authenticated identity."""
    ctx.obj.britive.set_output_format(None if output_format is None else output_format.value)
    ctx.obj.britive.list_secrets()


@app.callback()
def ls():
    """
    Lists resources available to the the currently authenticated identity.
    """
