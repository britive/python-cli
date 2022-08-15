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
        'browser'                   # when console access is checked out open the browser to the URL provided
    ],
    case_sensitive=False
)

