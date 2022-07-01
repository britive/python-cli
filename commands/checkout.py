from typing import Optional
import typer
from helpers.inject_common_options import inject_common_options
from arguments.profile import ProfileArgument
from enums.mode import Mode
from options.alias import AliasOption
from options.mode import ModeOption

app = typer.Typer(add_completion=False)


@app.callback(invoke_without_command=True)
@inject_common_options
def checkout(
        ctx: typer.Context,
        profile: Optional[str] = ProfileArgument,
        alias: Optional[str] = AliasOption,
        mode: Optional[Mode] = ModeOption
):
    """
    Checkout a profile.
    """
    if not profile:  # build the profile via interactive prompts
        pass


if __name__ == "__main__":
    app()
