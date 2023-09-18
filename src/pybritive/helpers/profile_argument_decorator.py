import click
import pkg_resources
from ..completers.profile import profile_completer

click_major_version = int(pkg_resources.get_distribution('click').version.split('.')[0])


def click_smart_profile_argument(func):
    if click_major_version >= 8:
        dec = click.argument('profile', shell_complete=profile_completer)
    else:
        dec = click.argument('profile')
    return dec(func)
