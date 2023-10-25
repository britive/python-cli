import click
import pkg_resources
from ..completers.profile import profile_completer
import os
import json


click_major_version = int(pkg_resources.get_distribution('click').version.split('.')[0])


def validate_profile(ctx, param, value):
    if 'KUBERNETES_EXEC_INFO' in os.environ:
        try:
            return json.loads(os.getenv('KUBERNETES_EXEC_INFO'))['spec']['cluster']['config']['britive-profile']
        except:
            raise ValueError('unable to find britive profile via cluster exec-extension with name britive-profile')
    return value


def is_required():
    return 'KUBERNETES_EXEC_INFO' not in os.environ


def click_smart_profile_argument(func):
    required = is_required()
    kwargs = {
        'required': required
    }
    if not required:
        kwargs['callback'] = validate_profile
    if click_major_version >= 8:
        kwargs['shell_complete'] = profile_completer

    dec = click.argument(
        'profile',
        **kwargs
    )
    return dec(func)
