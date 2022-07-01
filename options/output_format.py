import typer


OutputFormatOption = typer.Option(
    None, '-f', '--format',
    help=(
        'Display output format. Valid values are (json, yaml, csv, table[_format]). '
        'If `table` is used an optional table format can be specified as `table_format`. '
        'Valid table formats can be found here: https://github.com/astanin/python-tabulate#table_format. '
        'Example: `table_pretty`.'
    ),
    show_choices=True,
    case_sensitive=False,
)