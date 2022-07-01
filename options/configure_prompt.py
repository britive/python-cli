import typer

ConfigurePrompt = typer.Option(
    False, '-P/ ', '--no-prompt/ ',
    help='Do not prompt for any missing data. Used when programmatically running `configure [tenant|global]`.'
)
