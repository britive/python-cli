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
            'spec': {
                'cluster': {
                    'server': 'https://AFEA586304825E6AE82B38EA8B8665D2.gr7.us-west-1.eks.amazonaws.com',
                    'certificate-authority-data': 'LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJek1EUXhNREUwTkRRd01Wb1hEVE16TURRd056RTBORFF3TVZvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTTZUCk93Q25NclkzK0lhY1ZqUFpGYitxdi9GT1ZtQVJhOGVjZXNvN0VlblhOT1hod05sNjF6Ykk0UGhVcjRwU2U5QU8KTGwwd0lBUkZheWdtdTk4YVc0bU44UjcyYkVLc041WlYvL2FNbTdwTVJab2dYRDdNWDFseVNqRzdYUDgzRzBVYQpXMGlhS0JPdE96Q0F6dzBOVXAzd0E5ZzV5bUNIeGk2V3ZMZHRWOU9PSnlKYjkzM3NDZGhsM3phWlN6QmlzL1daClJsU0xIODlveUZXY0w5NGF2UU1WeGRGZHg2TlFLZ0ZnMERsMXNGTlFYbFlTbXkyUS8zd3lubU1RSlZqcnV6a2gKUW1yNDRoSUNrUmtZQVd5OU1wR2kwSmswa0IrekkwQzZnWWhqOG1OTS9wZEk3Skd0OXBCWWMrOWdnYVRuQWN5SQpGMWxDYjNVYlQ0VU4vcXZqMFkwQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZPQi94ZXdrRENVaDA0Y2QvcXpHN0JJbFAzOGdNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnRUJBSTV5T2FrMzNpanhhakZ4TkloNQpkek1iNVlxY1c1RlNUMmJOQlhITzQvSjRjNUduVWFvV1FDZnNJK0FHQ0tBMXl5WUxIZmJwVEt2TjNGUW9rWGlSCi9oSG1reGJqMTk2MlEwZDFWSkExdk1nUktLa3lBOTZYQ1UrN3hxci9HeExzN1huTWphNHhrcEJKaEw0RSt6b1kKNy9PcEZxR2ZpUitoSmtncWN1MTlQenczZmN4VVdDZHlLSjNNZVMwN1psTzZLMjBONnoxUUFrNXA3Mi9BTERnQgpHWTVUVFhmU2tHakhyU1pMWnVjb25ZM1BSci9iWmRGNEhUdWhHZzJ2aXA2SytCWjJLQUpURDBlUkQvYTRpY1pMCjl6R09YU21Hc1krakpDY0l5VnBrenpsdGczMVNHc0NCOEtPTlU4YzRhb0RJWVhOSnFybjRmYm5YZnI0VVEwam4KZmtZPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg=='
                }
            },
            'status': {
                'expirationTimestamp': credentials['expirationTime'],
                'token': credentials['jwt']
            }
        }
        return json.dumps(response)
