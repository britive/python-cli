import click


option = click.option(
    '--gcloud-key-file',
    default=None,
    help='GCP Programmatic Only - When mode is `gcloudauth` specify a non-default location for storing the key file.',
    show_default=True
)
