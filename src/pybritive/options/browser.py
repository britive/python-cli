import click
from ..choices.browser import browser_choices


# as of v1.1.0 not setting a default value here on purpose as the config file now has an
# aws section which provides a default value if the --mode option is omitted
# the default to `json` will occur now in helpers/cloud_credential_printer::CloudCredentialPrinter.__init__
option = click.option(
    '--browser',
    type=browser_choices,
    default=None,
    show_choices=True,
    help='The browser to use when opening a URL from the PyBritive CLI. Defaults to None which indicates the standard '
         'webbrowser selection process should be used.'
)
