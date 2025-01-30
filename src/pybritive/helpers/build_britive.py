from dataclasses import dataclass
from functools import wraps

import click
from click import Context
from merge_args import merge_args

from pybritive.britive_cli import BritiveCli


@dataclass
class Common:
    britive: BritiveCli


def should_set_output_format(ctx: Context) -> bool:
    parent_command = ctx.parent.command.name
    command = ctx.command.name
    return not ((parent_command in ['configure', 'clear']) or (parent_command == 'cache' and command in ['clear']))


# this wrapper exists to centralize all "common" CLI options (options that exist for all commands)
def build_britive(f):
    @merge_args(f)
    @wraps(f)
    @click.pass_context
    def wrapper(ctx, **kwargs):
        ctx.obj = Common(
            BritiveCli(
                tenant_name=kwargs.get('tenant'),
                token=kwargs.get('token'),
                silent=kwargs.get('silent', False),
                passphrase=kwargs.get('passphrase'),
                federation_provider=kwargs.get('federation_provider'),
            )
        )
        if should_set_output_format(ctx=ctx):
            ctx.obj.britive.set_output_format(kwargs.get('output_format'))
        return f(ctx=ctx, **kwargs)

    return wrapper
