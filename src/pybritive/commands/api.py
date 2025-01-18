import click
from click import Command

from pybritive.completers.api_command import command_api_patch_shell_complete
from pybritive.helpers.api_method_argument_decorator import click_smart_api_method_argument
from pybritive.helpers.build_britive import build_britive
from pybritive.options.britive_options import britive_options

# this holds all the click version logic to gracefully degrade functionality
# depending on the click version
command_api_patch_shell_complete(Command)


@click.command(context_settings={'ignore_unknown_options': True, 'allow_extra_args': True})
@build_britive
@britive_options(names='query,output_format,tenant,token,silent,passphrase,federation_provider')
@click_smart_api_method_argument  # need to gracefully handle older version of click
def api(ctx, query, output_format, tenant, token, silent, passphrase, federation_provider, method):
    """Exposes the Britive Python SDK methods to the CLI.

    Documentation on each SDK method can be found inside the Python SDK itself and on Github
    (https://github.com/britive/python-sdk). The Python package `britive` is a dependency of the CLI
    already so the SDK is available without installing any extra packages.

    It is left up to the caller to provide the proper `method` and `parameters` based on the documentation
    of the API call being performed.

    The authenticated identity must have the appropriate permissions to perform the actions being requested.
    General end users of Britive will not have these permissions. This call (and the larger SDK) is generally
    meant for administrative functionality.

    Example of use:

    * generic: pybritive api method --parameter1 value1 --parameter2 value2 [--parameterX valueX]

    * pybritive api users.list

    * pybritive api tags.create --name testtag --description "test tag"

    * pybritive api users.list --query '[].email'

    * pybritive api profiles.create --application-id <id> --name testprofile

    """
    parameters = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
    ctx.obj.britive.api(method=method, parameters=parameters, query=query)
