import click

from pybritive.choices.mode import mode_choices

# as of v1.1.0 not setting a default value here on purpose as the config file now has an
# aws section which provides a default value if the --mode option is omitted
# the default to `json` will occur now in helpers/cloud_credential_printer::CloudCredentialPrinter.__init__
option = click.option(
    '--mode',
    '-m',
    type=mode_choices,
    show_choices=True,
    help='How checked out credentials are presented. Defaults to `json` if not provided. '
    'General: `json` (JSON output), `text` (plain key-value output). '
    'AWS: `env` (eval-able export/set statements, auto-detects OS), `env-nix` (export for Linux/Mac), '
    '`env-wincmd` (set for Windows cmd), `env-winps` ($Env: for PowerShell), '
    '`integrate` (write credentials to ~/.aws/credentials), '
    '`awscredentialprocess` (credential_process JSON format for ~/.aws/config, with caching). '
    'Azure: `azlogin` (eval-able `az login` command), `azps` (PowerShell login script). '
    'GCP: `gcloudauth` (saves key file, outputs eval-able `gcloud auth activate-service-account` command), '
    '`gcloudauthexec` (same as gcloudauth but executes the command directly in a subprocess). '
    'OpenShift: `os-oclogin` (performs OIDC auth code grant flow, outputs eval-able `oc login` command), '
    '`os-ocloginexec` (same as os-oclogin but executes `oc login` directly in a subprocess). '
    'Kubernetes: `kube-exec` (ExecCredential output for kubeconfig OIDC exec plugin, with caching). '
    'Console/Browser: `console` (prints console URL), `browser` (opens URL in default browser), '
    '`browser-<name>` (opens URL in a specific browser, e.g. browser-chrome, browser-firefox).',
)
