import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.group()
def aws():
    """Groups together AWS specific sub-commands. Naming conventions will change to support standard AWS names."""
    pass


@aws.command()
@build_britive
@britive_options(names='aws_profile,aws_console_duration,browser')
def console(ctx, profile, duration, browser):
    """Signs an AWS console federation URL with AWS access keys and opens the AWS console in a browser."""

    ctx.obj.britive.aws_console(
        profile=profile,
        duration=duration,
        browser=browser
    )
