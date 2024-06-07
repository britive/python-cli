import base64
import os
from pathlib import Path
import shutil
import yaml
from .config import ConfigManager
from ..britive_cli import BritiveCli


def sanitize(name: str):
    name = name.lower()
    # name = name.replace(' ', '_').replace('/', "_").replace('\\', '_')
    return name


def check_env_var(filename, cli: BritiveCli):
    kubeconfig = os.getenv('KUBECONFIG')

    # no env var present
    if not kubeconfig:
        command = f'export KUBECONFIG=~/.kube/config:{filename}'
        cli.print('Please ensure your KUBECONFIG environment variable includes the Britive managed kube config file.')
        cli.print(command)
    else:
        for configfile in kubeconfig.split(':'):
            full_path = str(Path(configfile).expanduser()).lower()
            if filename.lower() == full_path:
                return  # we found what we came for - silently continue

        # if we get here we need to instruct the user to add the britive managed kube config file
        cli.print('Please modify your KUBECONFIG environment variable to include the Britive managed kube config file.')
        command = f'export KUBECONFIG="${{KUBECONFIG}}:{filename}"'
        cli.print(command)


def merge_new_with_existing(clusters, contexts, users, filename, tenant):
    # get the existing config, so we can pop out all
    # items related to this tenant as we will be replacing
    # them with the above created items
    existing_kubeconfig = {}
    if Path(filename).exists():
        with open(filename, 'r', encoding='utf-8') as f:
            existing_kubeconfig = yaml.safe_load(f) or {}

    prefix = f'{tenant}-'
    for cluster in existing_kubeconfig.get('clusters', []):
        if not cluster.get('name', '').startswith(prefix):
            clusters.append(cluster)

    for context in existing_kubeconfig.get('contexts', []):
        cluster_name = context.get('context', {}).get('cluster', '')
        if not cluster_name.startswith(prefix):
            contexts.append(context)

    for user in existing_kubeconfig.get('users', []):
        if not user.get('name', '').startswith(prefix):
            users.append(user)

    kubeconfig = {'apiVersion': 'v1', 'clusters': clusters, 'contexts': contexts, 'users': users, 'kind': 'Config'}

    # write out the config file
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.safe_dump(kubeconfig, f, default_flow_style=False, encoding='utf-8')


def parse_profiles(profiles, aliases):
    cluster_names = {}
    assigned_aliases = []
    for profile in profiles:
        env_profile = f"{sanitize(profile['env'])}-{sanitize(profile['profile'].lower())}"
        if env_profile not in cluster_names:
            app = BritiveCli.escape_profile_element(profile['app'])
            env = BritiveCli.escape_profile_element(profile['env'])
            pro = BritiveCli.escape_profile_element(profile['profile'])

            escaped_profile_str = f"{app}/{env}/{pro}".lower()
            alias = aliases.get(escaped_profile_str, None)
            assigned_aliases.append(alias)

            cluster_names[env_profile] = {
                'apps': [],
                'url': profile['url'],
                'cert': profile['cert'],
                'escaped_profile': escaped_profile_str,
                'profile': f"{profile['app']}/{profile['env']}/{profile['profile']}".lower(),
                'alias': alias,
            }
        cluster_names[env_profile]['apps'].append(sanitize(profile['app']))
    return [cluster_names, assigned_aliases]


def valid_cert(cert: str, profile: str, cli: BritiveCli):
    try:
        decoded_cert = base64.b64decode(cert).decode('utf-8')
        if not decoded_cert.startswith('-----BEGIN CERTIFICATE-----'):
            raise ValueError()
        if not decoded_cert.strip().endswith('-----END CERTIFICATE-----'):
            raise ValueError()
        return True
    except Exception:
        cli.print(f'could not properly decode certificate authority data for profile {profile} - skipping this cluster')
        return False


def build_tenant_config(tenant, cluster_names, username, cli: BritiveCli):
    kube_exec_full_path = shutil.which('pybritive-kube-exec')
    if not kube_exec_full_path:
        kube_exec_full_path = 'pybritive-kube-exec'
    users = (
        [
            {
                'name': username,
                'user': {
                    'exec': {
                        'apiVersion': 'client.authentication.k8s.io/v1beta1',
                        'command': kube_exec_full_path,
                        'args': ['-t', tenant],
                        'env': None,
                        'interactiveMode': 'Never',
                        'provideClusterInfo': True,
                    }
                },
            }
        ]
        if len(cluster_names.keys()) > 0
        else []
    )
    contexts = []
    clusters = []

    for env_profile, details in cluster_names.items():
        if len(details['apps']) == 1:
            names = [env_profile]
        else:
            names = [f"{sanitize(a)}-{env_profile}" for a in details['apps']]

        cert = details['cert']
        url = details['url']

        if not valid_cert(cert=cert, profile=details['profile'], cli=cli):
            continue

        for name in names:
            clusters.append(
                {
                    'name': f'{tenant}-{name}',
                    'cluster': {
                        'certificate-authority-data': cert,
                        'server': url,
                        'extensions': [
                            {
                                'name': 'client.authentication.k8s.io/exec',
                                'extension': {'britive-profile': details.get('alias') or details['escaped_profile']},
                            }
                        ],
                    },
                }
            )

            contexts.append(
                {
                    'name': details.get('alias') or f'{tenant}-{name}',
                    'context': {'cluster': f'{tenant}-{name}', 'user': username},
                }
            )
    return [clusters, contexts, users]


def build_kube_config(profiles: list, config: ConfigManager, username: str, cli: BritiveCli):
    tenant = config.get_tenant()['alias'].lower()  # must be run first to set the tenant alias in the config

    # something unique that is not likely to clash with any other username that may be present in a kube config file
    # add the tenant details which will mean 1 user per tenant
    username = f'{tenant}-{username}'

    # grab the aliases
    aliases = config.get_profile_aliases(reverse_keys=True)

    # parse all the profiles
    cluster_names, assigned_aliases = parse_profiles(profiles, aliases)

    # establish the 3 elements of the config
    clusters, contexts, users = build_tenant_config(
        tenant=tenant, cluster_names=cluster_names, username=username, cli=cli
    )

    # calculate the path for the config
    kube_dir = Path(config.base_path) / 'kube'
    kube_dir.mkdir(exist_ok=True)
    filename = str(kube_dir / 'config')

    # merge any existing config with the new config
    # and write it to disk
    merge_new_with_existing(clusters=clusters, contexts=contexts, users=users, tenant=tenant, filename=filename)

    # if required ensure we tell the user they need to modify their KUBECONFIG env var
    # in order to pick up the Britive managed kube config file
    if len(clusters) > 0:
        check_env_var(filename=filename, cli=cli)
