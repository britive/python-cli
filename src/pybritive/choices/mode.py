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
        'browser-chromium'
    ],
    case_sensitive=False
)
