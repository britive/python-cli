import click
from ..choices.output_format import output_format_choices


option = click.option(
    '--format', '-f', 'output_format',  # format is a reserved word so method parameter will be output_format
    default=None,
    help=(
        'Display output format. Valid values are (json, yaml, csv, table[-format]). '
        'If `table` is used an optional table format can be specified as `table-format`. '
        'Valid table formats can be found here: https://github.com/astanin/python-tabulate#table_format. '
        'Example: `table-pretty`.'
    ),
    show_choices=True,
    type=output_format_choices,
    show_default=True

)

