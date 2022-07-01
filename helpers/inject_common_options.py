from typing import Callable, Optional
from britive_cli import BritiveCli
import typer
from functools import wraps
from merge_args import merge_args
from dataclasses import dataclass
from options.tenant import TenantOption


# to be used to inject additional information into the typer.Context ctx.obj
@dataclass
class Common:
    britive: BritiveCli


# this wrapper exists to centralize all "common" CLI options (options that exist for all commands)
# adapted from https://github.com/tiangolo/typer/issues/296
def inject_common_options(f: Callable):
    @merge_args(f)
    @wraps(f)
    def wrapper(
            ctx: typer.Context,
            tenant: Optional[str] = TenantOption,
            **kwargs
    ):
        ctx.obj = Common(BritiveCli(tenant_name=tenant, token=kwargs.get('token')))
        return f(ctx=ctx, **kwargs)
    return wrapper
