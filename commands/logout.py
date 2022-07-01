import typer
from helpers.inject_common_options import inject_common_options


app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
@inject_common_options
def logout(ctx: typer.Context):
    """
    Logout of an interactive login session.

    This only applies when an API token has not been specified via --token,-T or via environment variable
    BRITIVE_API_TOKEN.
    """
    ctx.obj.britive.logout()
