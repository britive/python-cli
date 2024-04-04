import click

# eval example: eval $(pybritive checkout test -m env)

mode_choices = click.Choice(
    [
        'text',                     # text based output
        'json',                     # json based output
        'env',                      # environment variable output (suitable for eval)
        'integrate',                # stick the credentials into the local CSP credentials file (AWS)
        'env-nix',                  # environment variable output specifying "export"
        'env-wincmd',               # environment variable output specifying "set"
        'env-winps',                # environment variable output specifying "$env:"
        'awscredentialprocess',     # aws credential process output with additional caching to make the credential process more performant
        'azlogin',                  # azure az login command with all fields populated (suitable for eval)
        'azps',                     # azure powershell script
        'browser',                  # checkout console access (without having to specify --console/-c) and open the default browser to the URL provided in the checkout
        'gcloudauth',               # gcloud auth activate-service-account with all fields populated (suitable for eval)
        'console',                  # checkout console access (without having to specify --console/-c) and print the URL
        'browser-mozilla',
        'browser-firefox',
        'browser-windows-default',
        'browser-macosx',
        'browser-safari',
        'browser-chrome',
        'browser-chromium',
        'kube-exec',                # bake into kubeconfig with oidc exec output and additional caching to make kubectl more performant
        'gcloudauthexec',           # will effectively execute results of gcloudauth in a sub-shell
        'os-oclogin',               # will attempt an oidc authorization code grant flow for generating the `oc login ...` command for OpenShift
        'os-ocloginexec',           # will attempt an oidc authorization code grant flow for generating the `oc login ...` command for OpenShift and exec the result in a subshell
    ],
    case_sensitive=False
)
