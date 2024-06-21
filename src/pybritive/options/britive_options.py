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
from ..options.otp import option as otp
from ..options.silent import option as silent
from ..options.console import option as console
from ..options.checked_out import option as checked_out
from ..options.file import option as file
from ..options.configure_backend import option as configure_backend
from ..options.passphrase import option as passphrase
from ..options.force_renew import option as force_renew
from ..options.aws_credentials_file import option as aws_credentials_file
from ..options.federation_provider import option as federation_provider
from ..options.gcloud_key_file import option as gcloud_key_file
from ..options.verbose import option as verbose
from ..options.query import option as query
from ..options.ssh_hostname import option as ssh_hostname
from ..options.ssh_username import option as ssh_username
from ..options.ssh_push_public_key import option as ssh_push_public_key
from ..options.ssh_port import option as ssh_port
from ..options.ssh_key_source import option as ssh_key_source
from ..options.aws_profile import option as aws_profile
from ..options.aws_console_duration import option as aws_console_duration
from ..options.browser import option as browser
from ..options.extend import option as extend
from ..options.profile_type import option as profile_type


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
    'otp': otp,
    'silent': silent,
    'console': console,
    'checked_out': checked_out,
    'file': file,
    'configure_backend': configure_backend,
    'passphrase': passphrase,
    'force_renew': force_renew,
    'aws_credentials_file': aws_credentials_file,
    'federation_provider': federation_provider,
    'gcloud_key_file': gcloud_key_file,
    'verbose': verbose,
    'query': query,
    'ssh_hostname': ssh_hostname,
    'ssh_username': ssh_username,
    'ssh_push_public_key': ssh_push_public_key,
    'ssh_port': ssh_port,
    'ssh_key_source': ssh_key_source,
    'aws_profile': aws_profile,
    'aws_console_duration': aws_console_duration,
    'browser': browser,
    'extend': extend,
    'profile_type': profile_type
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
