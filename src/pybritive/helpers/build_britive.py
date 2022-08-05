from ..britive_cli import BritiveCli
import click
from functools import wraps
from merge_args import merge_args
from dataclasses import dataclass


@dataclass
class Common:
    britive: BritiveCli


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
            passphrase=kwargs.get('passphrase')
        ))

        parent_command = ctx.parent.command.name
        if parent_command != 'configure':
            ctx.obj.britive.set_output_format(kwargs.get('output_format'))
        return f(ctx=ctx, **kwargs)
    return wrapper
