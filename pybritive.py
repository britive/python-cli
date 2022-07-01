from typing import Optional
import typer
import commands.configure as configure
import commands.login as login
import commands.logout as logout
import commands.ls as ls
import commands.user as user
import commands.checkout as checkout
from options.version import VersionOption, version_callback

app = typer.Typer(add_completion=False)
app.add_typer(configure.app, name="configure")
app.add_typer(login.app, name="login")
app.add_typer(logout.app, name="logout")
app.add_typer(ls.app, name="ls")
app.add_typer(user.app, name="user")
app.add_typer(checkout.app, name="checkout")


@app.command()
def version():
    """Prints the PyBritive CLI version."""
    version_callback(True)


# this is the "main" app - it really does nothing but print the overview/help section
# all CLI functions are handled by the various commands, as decorated by @app.command()
@app.callback()
def base(cli_version: Optional[bool] = VersionOption):
    """
    PyBritive CLI - Pure Python Implementation for a Britive CLI
    """


if __name__ == "__main__":
    app()
