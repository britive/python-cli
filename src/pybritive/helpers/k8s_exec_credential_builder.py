import json
import os


class KubernetesExecCredentialProcessor:
    def __init__(self):
        self.api_version = None
        self.profile = None
        self.exec_data = None
        self._parse()

    def _parse(self):
        # parse the information provided by kube exec
        self.exec_data = json.loads(os.environ.get('KUBERNETES_EXEC_INFO', 'null'))

        if not self.exec_data:  # this env var HAS to exist if we are being invoked by k8s kubeconfig exec command
            raise Exception(
                'could not find environment variable KUBERNETES_EXEC_INFO - is this command being run '
                'within a kubeconfig context?'
            )

        self.api_version = self.exec_data.get('apiVersion')

        if not self.api_version:
            raise ValueError('apiVersion not found. Cannot continue.')

        if self.api_version == 'client.authentication.k8s.io/v1alpha1':
            raise ValueError(f'apiVersion {self.api_version} is not supported.')

        if self.api_version not in ['client.authentication.k8s.io/v1', 'client.authentication.k8s.io/v1beta1']:
            raise Exception(f'apiVersion {self.api_version} not accounted for.')

        self.profile = self.exec_data.get('spec', {}).get('cluster', {}).get('config', {}).get('britive-profile')

        if not self.profile:
            raise ValueError(
                'kubeconfig cluster extension named britive-profile not found or no profile value specified'
            )

    def construct_exec_credential(self, credentials: dict):
        response = {
            'kind': 'ExecCredential',
            'apiVersion': self.api_version,
            'spec': {},
            'status': {'expirationTimestamp': credentials['expirationTime'], 'token': credentials['jwt']},
        }
        return json.dumps(response)
