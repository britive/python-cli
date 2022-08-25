import click
from ..options.tenant import option as tenant
from ..options.token import option as token
from ..options.output_format import option as output_format
from ..options.alias import option as alias
from ..options.blocktime import option as blocktime
from ..options.mode import option as mode
from ..options.maxpolltime import option as maxpolltime
from ..options.version import option as version
from ..options.configure_tenant import option as configure_tenant
from ..options.configure_alias import option as configure_alias
from ..options.configure_prompt import option as configure_prompt
from ..options.justification import option as justification
from ..options.silent import option as silent
from ..options.console import option as console
from ..options.checked_out import option as checked_out
from ..options.file import option as file
from ..options.configure_backend import option as configure_backend
from ..options.passphrase import option as passphrase
from ..options.force_renew import option as force_renew
from ..options.aws_credentials_file import option as aws_credentials_file

options_map = {
    'tenant': tenant,
    'token': token,
    'format': output_format,
    'output_format': output_format,
    'alias': alias,
    'blocktime': blocktime,
    'mode': mode,
    'maxpolltime': maxpolltime,
    'version': version,
    'configure_tenant': configure_tenant,
    'configure_alias': configure_alias,
    'configure_prompt': configure_prompt,
    'justification': justification,
    'silent': silent,
    'console': console,
    'checked_out': checked_out,
    'file': file,
    'configure_backend': configure_backend,
    'passphrase': passphrase,
    'force_renew': force_renew,
    'aws_credentials_file': aws_credentials_file
}


def britive_options(*args, **kwargs):
    def inner(f):
        names = [n.strip() for n in kwargs['names'].split(',')]
        names.reverse()
        for name in names:
            option = options_map.get(name)
            if not name:
                raise click.ClickException(f'Invalid option {name} provided.')
            f = option(f)
        return f
    return inner

