import click

from pybritive.options.alias import option as alias
from pybritive.options.aws_console_duration import option as aws_console_duration
from pybritive.options.aws_credentials_file import option as aws_credentials_file
from pybritive.options.aws_profile import option as aws_profile
from pybritive.options.blocktime import option as blocktime
from pybritive.options.browser import option as browser
from pybritive.options.checked_out import option as checked_out
from pybritive.options.configure_alias import option as configure_alias
from pybritive.options.configure_backend import option as configure_backend
from pybritive.options.configure_prompt import option as configure_prompt
from pybritive.options.configure_tenant import option as configure_tenant
from pybritive.options.console import option as console
from pybritive.options.extend import option as extend
from pybritive.options.federation_provider import option as federation_provider
from pybritive.options.file import option as file
from pybritive.options.force_renew import option as force_renew
from pybritive.options.gcloud_key_file import option as gcloud_key_file
from pybritive.options.justification import option as justification
from pybritive.options.maxpolltime import option as maxpolltime
from pybritive.options.mode import option as mode
from pybritive.options.otp import option as otp
from pybritive.options.output_format import option as output_format
from pybritive.options.passphrase import option as passphrase
from pybritive.options.profile_type import option as profile_type
from pybritive.options.query import option as query
from pybritive.options.silent import option as silent
from pybritive.options.ssh_hostname import option as ssh_hostname
from pybritive.options.ssh_key_source import option as ssh_key_source
from pybritive.options.ssh_port import option as ssh_port
from pybritive.options.ssh_push_public_key import option as ssh_push_public_key
from pybritive.options.ssh_username import option as ssh_username
from pybritive.options.tenant import option as tenant
from pybritive.options.ticket_id import option as ticket_id
from pybritive.options.ticket_type import option as ticket_type
from pybritive.options.token import option as token
from pybritive.options.verbose import option as verbose
from pybritive.options.version import option as version

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
    'ticket_type': ticket_type,
    'ticket_id': ticket_id,
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
    'profile_type': profile_type,
}


def britive_options(**kwargs):
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
