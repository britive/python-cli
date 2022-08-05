import click


option = click.option(
    '-P/ ', '--no-prompt/ ', 'configure_prompt',
    default=False,
    show_default=True,
    is_flag=True,
    help='Do not prompt for any missing data. Used when programmatically running `configure [tenant|global]`.'
)
