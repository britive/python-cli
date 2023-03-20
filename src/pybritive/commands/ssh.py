import click
from ..helpers.build_britive import build_britive
from ..options.britive_options import britive_options


@click.group()
def ssh():
    """Facilitates connecting to private cloud servers using the standard ssh protocol."""
    pass


@ssh.group()
def aws():
    """Facilitates connecting, via SSH, to private AWS EC2 instances via Session Manager and EC2 Instance Connect.

    This command generally should be called from within an SSH config as opposed to being directly invoked.
    """
    pass


@aws.command()
@build_britive
@britive_options(names='ssh_username,ssh_hostname,ssh_push_public_key,ssh_port,ssh_key_source')
def ssm_proxy(ctx, username, hostname, push_public_key, port_number, key_source):
    """Outputs AWS CLI command to be consumed by ProxyCommand to establish an SSH proxy tunnel."""
    ctx.obj.britive.ssh_aws_ssm_proxy(
        username=username,
        hostname=hostname,
        push_public_key=push_public_key,
        port_number=port_number,
        key_source=key_source
    )
