import click

from pybritive.choices.ssh_push_public_key import ssh_push_public_key_choices


def validate(ctx, param, value):
    cloud = str(ctx.parent.command.name)
    if value == 'default' and cloud == 'aws':
        return 'ec2-instance-connect'
    if value == 'default' and cloud == 'gcp':
        return 'os-login'

    if cloud == 'aws' and value not in ['ec2-instance-connect', None]:
        raise click.BadParameter(f'value {value} is not allowed for aws')

    if cloud == 'gcp' and value not in ['os-login', 'instance-metadata', None]:
        raise click.BadParameter(f'value {value} is not allowed for gcp')

    return value


option = click.option(
    '--push-public-key',
    '-P',
    type=ssh_push_public_key_choices,
    is_flag=False,
    flag_value='default',
    required=False,
    help='Whether to push an ephemeral public key to the remote server.',
    callback=validate,
)
