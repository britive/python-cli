from dataclasses import dataclass
from functools import wraps

import click
from merge_args import merge_args
from ..britive_cli import BritiveCli
from click import Context


@dataclass
class Common:
    britive: BritiveCli


def should_set_output_format(ctx: Context) -> bool:
    parent_command = ctx.parent.command.name
    command = ctx.command.name
    if parent_command in ['configure', 'clear']:
        return False

    if parent_command == 'cache' and command in ['clear']:
        return False

    return True


# this wrapper exists to centralize all "common" CLI options (options that exist for all commands)
def build_britive(f):
    @merge_args(f)
    @wraps(f)
    @click.pass_context
    def wrapper(
            ctx,
            **kwargs
    ):
        ctx.obj = Common(BritiveCli(
            tenant_name=kwargs.get('tenant'),
            token=kwargs.get('token'),
            silent=kwargs.get('silent', False),
            passphrase=kwargs.get('passphrase'),
            federation_provider=kwargs.get('federation_provider')
        ))
        if should_set_output_format(ctx=ctx):
            ctx.obj.britive.set_output_format(kwargs.get('output_format'))
        return f(ctx=ctx, **kwargs)
    return wrapper
