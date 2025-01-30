from sys import argv, exit


def get_args():
    from getopt import getopt  # lazy load

    options = getopt(
        argv[1:], 't:T:p:F:hv', ['tenant=', 'token=', 'passphrase=', 'federation-provider=', 'help', 'version']
    )[0]

    args = {'tenant': None, 'token': None, 'passphrase': None, 'federation_provider': None}

    for opt, arg in options:
        if opt in ('-t', '--tenant'):
            args['tenant'] = arg
        if opt in ('-T', '--token'):
            args['token'] = arg
        if opt in ('-p', '--passphrase'):
            args['passphrase'] = arg
        if opt in ('-F', '--federation-provider'):
            args['federation_provider'] = arg
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-v', '--version'):
            from importlib.metadata import version
            from platform import platform, python_version  # lazy load

            cli_version = version('pybritive')
            print(f'pybritive: {cli_version} / platform: {platform()} / python: {python_version()}')
            exit(0)

    return args


def usage():
    print(f'Usage : {argv[0]} [-t/--tenant, -T/--token, -t/--passphrase, -F/--federation-provider]')
    exit(0)


def main():
    args = get_args()

    from .k8s_exec_credential_builder import KubernetesExecCredentialProcessor

    k8s_processor = KubernetesExecCredentialProcessor()

    from .cache import Cache  # lazy load

    creds = Cache(passphrase=args['passphrase']).get_credentials(profile_name=k8s_processor.profile, mode='kube-exec')
    if creds:
        from datetime import datetime  # lazy load

        expiration = datetime.fromisoformat(creds['expirationTime'].replace('Z', ''))
        now = datetime.utcnow()
        if now > expiration:  # creds have expired so set to none so new one get checked out
            creds = None
        else:
            print(k8s_processor.construct_exec_credential(creds))
            exit()

    if not creds:
        from pybritive.britive_cli import BritiveCli  # lazy load for performance purposes

        b = BritiveCli(
            tenant_name=args['tenant'],
            token=args['token'],
            passphrase=args['passphrase'],
            federation_provider=args['federation_provider'],
            silent=True,
            from_helper_console_script=True,
        )
        b.config.get_tenant()  # have to load the config here as that work is generally done elsewhere
        b.checkout(
            alias=None,
            blocktime=None,
            console=False,
            justification=None,
            mode='kube-exec',
            maxpolltime=None,
            profile=k8s_processor.profile,
            passphrase=args['passphrase'],
            force_renew=None,
            aws_credentials_file=None,
            gcloud_key_file=None,
            verbose=None,
            extend=False,
            otp=None,
        )
        exit()


if __name__ == '__main__':
    main()
