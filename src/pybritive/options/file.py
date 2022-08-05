import click


option = click.option(
    '--file', '-F',
    help='Path to a file where the contents of the secret file will be stored. Omitting this option will '
         'result in the file being saved to the current directory with the name provided when the secret '
         'file was initially uploaded. Providing `-` will print the contents of the secret file to stdout.'
)

