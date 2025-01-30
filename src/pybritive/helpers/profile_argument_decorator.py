import json
import os

import click

from pybritive.completers.profile import profile_completer


def validate_profile(ctx, param, value):
    if kube_exec_info := os.getenv('KUBERNETES_EXEC_INFO'):
        try:
            return json.loads(kube_exec_info)['spec']['cluster']['config']['britive-profile']
        except Exception as e:
            raise ValueError(
                'unable to find britive profile via cluster exec-extension with name britive-profile'
            ) from e
    return value


def is_required():
    return 'KUBERNETES_EXEC_INFO' not in os.environ


def click_smart_profile_argument(func):
    required = is_required()
    kwargs = {'required': required}
    if not required:
        kwargs['callback'] = validate_profile
    kwargs['shell_complete'] = profile_completer

    dec = click.argument('profile', **kwargs)
    return dec(func)
