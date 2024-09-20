import click

# eval example: eval $(pybritive checkout test -m env)

# explanations:
#     awscredentialprocess: aws credential process output with additional caching to make the credential process more
#         performant
#     azlogin: azure az login command with all fields populated (suitable for eval)
#     azps: azure powershell script
#     browser: checkout console access (without having to specify --console/-c) and open the default browser to the URL
#         provided in the checkout
#     console: checkout console access (without having to specify --console/-c) and print the URL
#     env: environment variable output (suitable for eval)
#     env-nix: environment variable output specifying "export"
#     env-wincmd: environment variable output specifying "set"
#     env-winps: environment variable output specifying "$env:"
#     gcloudauth: gcloud auth activate-service-account with all fields populated (suitable for eval)
#     gcloudauthexec: will effectively execute results of gcloudauth in a sub-shell
#     integrate: stick the credentials into the local CSP credentials file (AWS)
#     json: json based output
#     kube-exec: bake into kubeconfig with oidc exec output and additional caching to make kubectl more performant
#     os-oclogin: will attempt an oidc authorization code grant flow for generating the `oc login ...` command for
#         OpenShift
#     os-ocloginexec: will attempt an oidc authorization code grant flow for generating the `oc login ...` command for
#         OpenShift and exec the result in a subshell
#     text: text based output

mode_choices = click.Choice(
    [
        'awscredentialprocess',
        'azlogin',
        'azps',
        'browser',
        'browser-chrome',
        'browser-chromium',
        'browser-firefox',
        'browser-macosx',
        'browser-mozilla',
        'browser-safari',
        'browser-windows-default',
        'console',
        'env',
        'env-nix',
        'env-wincmd',
        'env-winps',
        'gcloudauth',
        'gcloudauthexec',
        'integrate',
        'json',
        'kube-exec',
        'os-oclogin',
        'os-ocloginexec',
        'text',
    ],
    case_sensitive=False,
)
