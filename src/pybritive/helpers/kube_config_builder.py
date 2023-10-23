import yaml
from pathlib import Path
from .config import ConfigManager
from ..britive_cli import BritiveCli
import random
import string


def sanitize(name: str):
    name = name.lower()
    name = name.replace(' ', '_').replace('/', "_").replace('\\', '_')
    return name


def build_kube_config(profiles: list, config: ConfigManager, username: str):
    # there will only ever be 1 user here, so we can hardcoded it

    # something unique that is not likely to clash with any other username that may be present in a kube config file
    username = f'britive-{username}'

    aliases = config.get_profile_aliases(reverse_keys=True)
    cluster_names = {}
    for profile in profiles:
        env_profile = f"{sanitize(profile['env'])}-{sanitize(profile['profile'].lower())}"
        if env_profile not in cluster_names:
            app = BritiveCli.escape_profile_element(profile['app'])
            env = BritiveCli.escape_profile_element(profile['env'])
            pro = BritiveCli.escape_profile_element(profile['profile'])

            escaped_profile_str = f"{app}/{env}/{pro}".lower()
            alias = aliases.get(escaped_profile_str, None)

            cluster_names[env_profile] = {
                'apps': [],
                'url': profile['url'],
                'cert': profile['cert'],
                'escaped_profile': escaped_profile_str,
                'profile': f"{profile['app']}/{profile['env']}/{profile['profile']}".lower(),
                'alias': alias
            }
        cluster_names[env_profile]['apps'].append(sanitize(profile['app']))

    users = [
        {
            'name': username,
            'user': {
                'exec': {
                    'apiVersion': 'client.authentication.k8s.io/v1beta1',
                    'command': 'pybritive-kube-exec',  # todo - somehow get full path? not sure it is required?
                    'env': None,
                    'interactiveMode': 'Never',
                    'provideClusterInfo': True
                }
            }
        }
    ]
    contexts = []
    clusters = []

    for env_profile, details in cluster_names.items():
        if len(details['apps']) == 1:
            names = [env_profile]
        else:
            names = [f"{sanitize(a)}-{env_profile}" for a in details['apps']]

        cert = details['cert']
        url = details['url']

        for name in names:
            clusters.append(
                {
                    'name': name,
                    'cluster': {
                        'certificate-authority-data': cert,
                        'server': url,
                        'extensions': [
                            {
                                'name': 'client.authentication.k8s.io/exec',
                                'extension': {
                                    'britive-profile': details.get('alias', details['escaped_profile'])
                                }
                            }
                        ]
                    }
                }
            )

            contexts.append(
                {
                    'name': details.get('alias', name),
                    'context': {
                        'cluster': name,
                        'user': username
                    }
                }
            )

    kubeconfig = {
        'apiVersion': 'v1',
        'clusters': clusters,
        'contexts': contexts,
        'users': users,
        'kind': 'Config'
    }

    kube_dir = Path(config.base_path) / 'kube'
    kube_dir.mkdir(exist_ok=True)
    filename = str(kube_dir / 'config')
    with open(filename, 'w') as f:
        yaml.dump(kubeconfig, f, default_flow_style=False)
