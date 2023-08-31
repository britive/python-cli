# register the completion scripts since they are not required to be registered anywhere else

import pkg_resources

# click < 8.0.0 does shell completion different...
# not all the classes/decorators are available, so we cannot
# create custom shell completions like we can with click > 8.0.0
click_major_version = int(pkg_resources.get_distribution('click').version.split('.')[0])
if click_major_version >= 8:
    from . import powershell_completion
    from . import bash_gte_42
