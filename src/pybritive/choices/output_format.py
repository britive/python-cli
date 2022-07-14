import click

output_format_choices = click.Choice(
    [
        'json',
        'yaml',
        'csv',
        'table',
        'list',
        'table-plain',
        'table-simple',
        'table-github',
        'table-grid',
        'table-simple_grid',
        'table-rounded_grid',
        'table-double_grid',
        'table-fancy_grid',
        'table-outline',
        'table-simple_outline',
        'table-rounded_outline',
        'table-double_outline',
        'table-fancy_outline',
        'table-pipe',
        'table-orgtbl',
        'table-jira',
        'table-presto',
        'table-pretty',
        'table-psql',
        'table-rst',
        'table-mediawiki',
        'table-moinmoin',
        'table-youtrack',
        'table-html',
        'table-unsafehtml',
        'table-latex',
        'table-latex_raw',
        'table-latex_booktabs',
        'table-latex_longtable',
        'table-textile',
        'table-tsv'
    ],
    case_sensitive=False
)

