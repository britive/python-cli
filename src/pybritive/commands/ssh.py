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


@ssh.group()
def gcp():
    """Facilitates connecting, via SSH, to private GCP Compute Instances via Identity Aware Proxy and OS Login/SSH Metadata.

    This command generally should be called from within an SSH config as opposed to being directly invoked.
    """
    pass


@aws.command()
@build_britive
@britive_options(names='ssh_push_public_key,ssh_key_source')
def config(ctx, push_public_key, key_source):
    """Prints the required Match directive to add to an OpenSSH config file (normally located at ~/.ssh/config.)"""

    ctx.obj.britive.ssh_aws_openssh_config(
        push_public_key=push_public_key,
        key_source=key_source
    )


@aws.command()
@build_britive
@britive_options(names='ssh_username,ssh_hostname,ssh_push_public_key,ssh_port,ssh_key_source')
def ssm_proxy(ctx, username, hostname, push_public_key, port_number, key_source):
    """Outputs AWS CLI command to be consumed by ProxyCommand to establish an OpenSSH proxy tunnel."""

    if push_public_key == 'default':
        push_public_key = True

    ctx.obj.britive.ssh_aws_ssm_proxy(
        username=username,
        hostname=hostname,
        push_public_key=push_public_key,
        port_number=port_number,
        key_source=key_source
    )


@gcp.command()
@build_britive
@britive_options(names='ssh_push_public_key,ssh_key_source')
def config(ctx, push_public_key, key_source):
    """Prints the required Match directive to add to an OpenSSH config file (normally located at ~/.ssh/config.)"""

    ctx.obj.britive.ssh_gcp_openssh_config(
        push_public_key=push_public_key,
        key_source=key_source
    )


@gcp.command()
@build_britive
@britive_options(names='ssh_username,ssh_hostname,ssh_push_public_key,ssh_port,ssh_key_source')
def identity_aware_proxy(ctx, username, hostname, push_public_key, port_number, key_source):
    """Outputs gcloud CLI command to be consumed by ProxyCommand to establish an OpenSSH proxy tunnel."""

    if push_public_key == 'default':
        push_public_key = 'os-login'

    ctx.obj.britive.ssh_gcp_identity_aware_proxy(
        username=username,
        hostname=hostname,
        push_public_key=push_public_key,
        port_number=port_number,
        key_source=key_source
    )
