import contextlib
import io
import os
import sys
from sys import argv


def _fallback_input(prompt='', stream=None):
    if not stream:
        stream = sys.stderr
    return _raw_input(prompt, stream)


def _linput(prompt='', stream=None):
    user_input = None
    with contextlib.ExitStack() as stack:
        try:
            fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
            tty = io.FileIO(fd, 'w+')
            stack.enter_context(tty)
            std_input = io.TextIOWrapper(tty)
            stack.enter_context(std_input)
            if not stream:
                stream = std_input
        except OSError:
            stack.close()
            try:
                fd = sys.stdin.fileno()
            except (AttributeError, ValueError):
                fd = None
                user_input = _fallback_input(prompt, stream)
            std_input = sys.stdin
            if not stream:
                stream = sys.stderr

        if fd is not None:
            try:
                old = termios.tcgetattr(fd)
                new = old[:]
                new[3] |= termios.ECHO
                tcsetattr_flags = termios.TCSAFLUSH
                if hasattr(termios, 'TCSASOFT'):
                    tcsetattr_flags |= termios.TCSASOFT
                try:
                    termios.tcsetattr(fd, tcsetattr_flags, new)
                    user_input = _raw_input(prompt, stream, std_input=std_input)
                finally:
                    termios.tcsetattr(fd, tcsetattr_flags, old)
                    stream.flush()
            except termios.error:
                if user_input is not None:
                    raise
                if stream is not std_input:
                    stack.close()
                user_input = _fallback_input(prompt, stream)

        stream.write('\n')
        return user_input


def _raw_input(prompt='', stream=None, std_input=None):
    if not stream:
        stream = sys.stderr
    if not std_input:
        std_input = sys.stdin
    prompt = str(prompt)
    if prompt:
        try:
            stream.write(prompt)
        except UnicodeEncodeError:
            prompt = prompt.encode(stream.encoding, 'replace')
            prompt = prompt.decode(stream.encoding)
            stream.write(prompt)
        stream.flush()
    line = std_input.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line


def _winput(prompt='', stream=None):
    if sys.stdin is not sys.__stdin__:
        return _fallback_input(prompt, stream)

    for c in prompt:
        msvcrt.putwch(c)
    user_input = ''
    while 1:
        c = msvcrt.getwche()
        if c in ('\r', '\n'):
            break
        if c == '\003':
            raise KeyboardInterrupt
        user_input = user_input[:-1] if c == '\x08' else user_input + c
    msvcrt.putwch('\r')
    msvcrt.putwch('\n')
    return user_input


try:
    import termios

    termios.tcgetattr, termios.tcsetattr  # noqa: B018
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        get_input = _fallback_input
    else:
        get_input = _winput
else:
    get_input = _linput


def get_args():
    from getopt import getopt  # lazy load

    options = getopt(
        argv[1:],
        't:T:p:f:P:F:hv',
        ['tenant=', 'token=', 'passphrase=', 'force-renew=', 'profile=', 'federation-provider=help', 'version'],
    )[0]

    args = {
        'tenant': None,
        'token': None,
        'passphrase': None,
        'force_renew': None,
        'profile': None,
        'federation_provider': None,
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
        if opt in ('-F', '--federation-provider'):
            args['federation_provider'] = arg
        if opt in ('-h', '--help'):
            usage()
        if opt in ('-v', '--version'):
            from importlib.metadata import version
            from platform import platform, python_version  # lazy load

            cli_version = version('pybritive')
            print(f'pybritive: {cli_version} / platform: {platform()} / python: {python_version()}')
            raise SystemExit

    return args


def usage():
    print(
        f'Usage : {argv[0]} --profile <profile> [-t/--tenant, -T/--token, -p/--passphrase, -f/--force-renew, '
        f'-F/--federation-provider]'
    )
    raise SystemExit


def perform_checkout(b, args, otp=None, justification=None):
    b.checkout(
        alias=None,
        blocktime=None,
        console=False,
        justification=justification,
        mode='awscredentialprocess',
        maxpolltime=None,
        profile=args['profile'],
        passphrase=args['passphrase'],
        force_renew=args['force_renew'],
        aws_credentials_file=None,
        gcloud_key_file=None,
        verbose=None,
        extend=False,
        otp=otp,
    )


def main():
    args = get_args()
    if not args['profile']:
        print('-P/--profile is required')
        usage()

    creds = None
    if not args['force_renew']:  # if force renew let's defer to that the full package vs. this helper
        from pybritive.helpers.cache import Cache  # lazy load

        creds = Cache(passphrase=args['passphrase']).get_credentials(
            profile_name=args['profile'], mode='awscredentialprocess'
        )
        if creds:
            from datetime import datetime  # lazy load

            expiration = datetime.fromisoformat(creds['expirationTime'].replace('Z', ''))
            now = datetime.utcnow()
            if now > expiration:  # creds have expired so set to none so new one get checked out
                creds = None
            else:  # not importing json library on purpose to keep imports down for speed
                json = '{'
                json += f'"AccessKeyId": "{creds["accessKeyID"]}",'
                json += f'"SecretAccessKey": "{creds["secretAccessKey"]}",'
                json += f'"SessionToken": "{creds["sessionToken"]}",'
                json += f'"Expiration": "{creds["expirationTime"]}",'
                json += '"Version": 1}'
                print(json)
                raise SystemExit
    if not creds:
        from britive import exceptions

        from pybritive.britive_cli import BritiveCli  # lazy load for performance purposes

        b = BritiveCli(
            tenant_name=args['tenant'],
            token=args['token'],
            passphrase=args['passphrase'],
            federation_provider=args['federation_provider'],
            silent=True,
            from_helper_console_script=True,
        )
        b.config.get_tenant()  # have to load the config here as that work is generally done

        try:
            perform_checkout(b, args)
        except exceptions.StepUpAuthRequiredButNotProvided:
            perform_checkout(b, args, otp=get_input(prompt='(pybritive) Enter OTP:'))
        except (
            exceptions.ApprovalRequiredButNoJustificationProvided,
            exceptions.badrequest.MissingJustificationError,
        ):
            try:
                perform_checkout(b, args, justification=get_input(prompt='(pybritive) Enter Justification: '))
            except exceptions.ProfileApprovalMaxBlockTimeExceeded as e:
                b.request_withdraw(profile=args['profile'])
                raise SystemExit('approval not settled before blocktime exceeded - request withdrawn') from e

        raise SystemExit


if __name__ == '__main__':
    main()
