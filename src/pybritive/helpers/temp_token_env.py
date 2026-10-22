import platform

from pybritive.helpers.cloud_credential_printer import env_options


def temp_token_env_lines(token: dict, tenant_url: str, mode: str) -> list[str]:
    modifier = mode.split('-', maxsplit=1)[1] if '-' in mode else None
    if not modifier:
        modifier = 'wincmd' if platform.system().lower() == 'windows' else 'nix'
    quote = '' if modifier == 'wincmd' else '"'  # cmd.exe keeps quotes as part of the value
    variables = {
        'BRITIVE_TENANT': tenant_url,
        'BRITIVE_TOKEN': token['accessToken'],
        'BRITIVE_TOKEN_EXPIRATION': token['expiresOn'],
    }
    return [f'{env_options[modifier]}{name}={quote}{value}{quote}' for name, value in variables.items()]
