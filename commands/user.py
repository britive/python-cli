import typer
from helpers.inject_common_options import inject_common_options
from options.token import TokenOption


app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
@inject_common_options
def user(
        ctx: typer.Context,
        token: str = TokenOption  # used by @inject common_options
):
    """
    Returns details about the authenticated identity.
    """
    ctx.obj.britive.user()
