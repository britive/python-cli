import typer
from helpers.inject_common_options import inject_common_options


app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
@inject_common_options
def login(ctx: typer.Context):
    """
    Perform an interactive login to obtain temporary credentials.

    This only applies when an API token has not been specified via --token,-T or via environment variable
    BRITIVE_API_TOKEN.
    """
    ctx.obj.britive.login(explicit=True)


if __name__ == "__main__":
    app()
