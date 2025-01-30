import click

from pybritive.helpers.build_britive import build_britive
from pybritive.helpers.profile_argument_decorator import click_smart_profile_argument


@click.group()
def clear():
    """Clear various local settings and configurations."""
    pass


@clear.command()
@build_britive
def cache(ctx):
    """Clears the local cache."""
    ctx.obj.britive.cache_clear()


@clear.command(name='kubeconfig')
@build_britive
def clear_kubeconfig(ctx):
    """Clears the local .britive/kube/config file."""
    ctx.obj.britive.clear_kubeconfig()


@clear.command(name='gcloud-auth-key-files')
@build_britive
def gcloud_auth_key_files(ctx):
    """Clears the local gcloud auth key files."""
    ctx.obj.britive.clear_gcloud_auth_key_files()


@clear.command(name='cached-aws-credentials')
@build_britive
@click_smart_profile_argument
def cached_aws_credentials(ctx, profile):
    """Clears cached AWS credentials used as part of the AWS CLI credential process."""
    ctx.obj.britive.clear_cached_aws_credentials(profile=profile)
