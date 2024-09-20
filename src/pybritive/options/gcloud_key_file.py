import click

option = click.option(
    '--gcloud-key-file',
    default=None,
    help=(
        'GCP Programmatic Only - When mode is `gcloudauth` specify a non-default location for storing the key file.'
        ' Ignored for mode `gcloudauthexec`.'
    ),
    show_default=True,
)
