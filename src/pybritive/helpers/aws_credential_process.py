def get_args():
    from getopt import getopt  # lazy load
    from sys import argv  # lazy load
    options, non_options = getopt(argv[1:], 't:T:p:f:P:hv', [
        'tenant=',
        'token=',
        'passphrase=',
        'force-renew=',
        'profile=',
        'help',
        'version'
    ])

    args = {
        'tenant': None,
        'token': None,
        'passphrase': None,
        'force_renew': None,
        'profile': None
    }

    for opt, arg in options:
        if opt in ('-t', '--tenant'):
            args['tenant'] = arg
        if opt in ('-T', '--token'):
            args['token'] = arg
        if opt in ('-p', '--passphrase'):
            args['passphrase'] = arg
        if opt in ('-f', '--force-renew'):
            args['force_renew'] = int(arg)
        if opt in ('-P', '--profile'):
            args['profile'] = arg
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-v', '--version'):
            from platform import platform, python_version  # lazy load
            from pkg_resources import get_distribution  # lazy load
            cli_version = get_distribution('pybritive').version
            print(
                f'pybritive: {cli_version} / platform: {platform()} / python: {python_version()}'
            )
            exit()

    return args


def usage():
    from sys import argv  # lazy load
    print("Usage : %s --profile <profile> [-t/--tenant, -T/--token, -t/--passphrase, -f/--force-renew]" % (argv[0]))
    exit()


def main():
    args = get_args()
    if not args['profile']:
        print('-P/--profile is required')
        usage()

    creds = None
    if not args['force_renew']:  # if force renew let's defer to that the full package vs. this helper
        from .cache import Cache  # lazy load
        creds = Cache(passphrase=args['passphrase']).get_awscredentialprocess(profile_name=args['profile'])
        if creds:
            from datetime import datetime  # lazy load
            expiration = datetime.fromisoformat(creds['expirationTime'].replace('Z', ''))
            now = datetime.utcnow()
            if now > expiration:  # creds have expired so set to none so new one get checked out
                creds = None
            else:
                json = '{'
                json += f'"AccessKeyId": "{creds["accessKeyID"]}",'
                json += f'"SecretAccessKey": "{creds["secretAccessKey"]}",'
                json += f'"SessionToken": "{creds["sessionToken"]}",'
                json += f'"Expiration": "{creds["expirationTime"]}",'
                json += '"Version": 1}'
                print(json)
                exit()
    if not creds:
        from ..britive_cli import BritiveCli  # lazy load for performance purposes

        b = BritiveCli(tenant_name=args['tenant'], token=args['token'], passphrase=args['passphrase'], silent=True)
        b.config.get_tenant()  # have to load the config here as that work is generally done
        b.checkout(
            alias=None,
            blocktime=None,
            console=False,
            justification=None,
            mode='awscredentialprocess',
            maxpolltime=None,
            profile=args['profile'],
            passphrase=args['passphrase'],
            force_renew=args['force_renew'],
            aws_credentials_file=None
        )
        exit()


if __name__ == '__main__':
    main()
