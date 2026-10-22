import click

# eval example: eval $(pybritive tokens create -m env)

# explanations:
#     env: environment variable output (suitable for eval)
#     env-nix: environment variable output specifying "export"
#     env-wincmd: environment variable output specifying "set"
#     env-winps: environment variable output specifying "$env:"

token_mode_choices = click.Choice(
    [
        'env',
        'env-nix',
        'env-wincmd',
        'env-winps',
    ],
    case_sensitive=False,
)
