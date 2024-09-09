import click

option = click.option(
    '--verbose', '-v', default=False, is_flag=True, show_default=True, help='Enable verbose checkout mode.'
)
