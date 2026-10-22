import platform
import time
from datetime import datetime

import click
import jwt

from pybritive.helpers.clipboard import copy_to_clipboard
from pybritive.helpers.cloud_credential_printer import env_options, safe_list_get


def _local_time(epoch: int) -> str:
    return datetime.fromtimestamp(epoch).astimezone().isoformat(timespec='seconds')


def _remaining(seconds: float) -> str:
    if seconds <= 0:
        return 'expired'
    hours, remainder = divmod(int(seconds), 3600)
    minutes = remainder // 60
    return f'{hours}h{minutes}m' if hours else f'{minutes}m'


def decode_token(token: str) -> dict:
    # inspection only - the signature is not verified
    try:
        header = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={'verify_signature': False})
    except jwt.exceptions.PyJWTError as e:
        raise click.ClickException(f'Unable to decode token: {e}') from e
    times = {}
    if 'iat' in payload:
        times['issued'] = _local_time(payload['iat'])
    if 'exp' in payload:
        times['expires'] = _local_time(payload['exp'])
        times['expiresIn'] = _remaining(payload['exp'] - time.time())
    return {'header': header, 'payload': payload, 'times': times}


class TempTokenPrinter:
    def __init__(self, mode, token, tenant_url, silent, cli):
        self.cli = cli
        self.silent = silent
        self.token = token
        self.tenant_url = tenant_url
        mode = mode or 'json'  # set a default if nothing is provided via flag --mode/-m
        self.mode = mode.split('-')[0]
        self.mode_modifier = safe_list_get(mode.split('-', maxsplit=1), 1, None)
        if self.mode == 'env':
            if not self.mode_modifier:
                self.mode_modifier = 'wincmd' if platform.system().lower() == 'windows' else 'nix'
            self.env_command = env_options[self.mode_modifier]

    def print(self):
        getattr(self, f'print_{self.mode}')()

    def _print_record(self, data: dict):
        output = [data] if self.cli.output_format in ['csv', 'list'] else data
        self.cli.print(output, ignore_silent=True)

    def print_json(self):
        self._print_record(self.token)

    def print_token(self):
        self.cli.print(self.token['accessToken'], ignore_silent=True)

    def print_decode(self):
        decoded = decode_token(self.token['accessToken'])
        if self.cli.output_format in ['json', 'yaml']:
            self.cli.print(decoded, ignore_silent=True)
        else:  # tabular formats need a flat record
            self._print_record({**decoded['payload'], **decoded['times']})

    def print_clipboard(self):
        copy_to_clipboard(self.token['accessToken'])
        if not self.silent:
            click.echo(f'Access token copied to clipboard (expires {self.token["expiresOn"]}).', err=True)

    def print_env(self):
        variables = {
            'BRITIVE_TENANT': self.tenant_url,
            'BRITIVE_TOKEN': self.token['accessToken'],
            'BRITIVE_TOKEN_EXPIRATION': self.token['expiresOn'],
        }
        quote = '' if self.mode_modifier == 'wincmd' else '"'  # cmd.exe keeps quotes as part of the value
        for name, value in variables.items():
            self.cli.print(f'{self.env_command}{name}={quote}{value}{quote}', ignore_silent=True)
