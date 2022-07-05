from typing import Optional
import typer
from helpers.inject_common_options import inject_common_options
from arguments.profile import ProfileArgument
from enums.mode import Mode
from options.alias import AliasOption
from options.mode import ModeOption
from options.blocktime import BlockTimeOption
from options.maxpolltime import MaxPollTimeOption


app = typer.Typer(add_completion=False)


@app.callback()
@inject_common_options
def checkout(
        ctx: typer.Context,
        profilename: str = ProfileArgument,
        alias: Optional[str] = AliasOption,
        mode: Mode = ModeOption,
        blocktime: int = BlockTimeOption,
        maxpolltime: int = MaxPollTimeOption
):
    """
    Checkout a profile.
    """
    if not profilename:  # build the profile via interactive prompts
        pass


if __name__ == "__main__":
    app()
