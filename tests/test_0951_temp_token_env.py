import pytest

from pybritive.helpers import temp_token_env
from pybritive.helpers.temp_token_env import temp_token_env_lines

TENANT_URL = 'https://example.britive-app.com'
TOKEN = {'accessToken': 'header.payload.signature', 'expiresOn': '2030-01-01T00:00:00.000Z'}


@pytest.mark.parametrize(
    'mode,prefix,quote',
    [('env-nix', 'export ', '"'), ('env-winps', '$Env:', '"'), ('env-wincmd', 'set ', '')],
)
def test_env_modes(mode, prefix, quote):
    assert temp_token_env_lines(TOKEN, tenant_url=TENANT_URL, mode=mode) == [
        f'{prefix}BRITIVE_TENANT={quote}{TENANT_URL}{quote}',
        f'{prefix}BRITIVE_TOKEN={quote}{TOKEN["accessToken"]}{quote}',
        f'{prefix}BRITIVE_TOKEN_EXPIRATION={quote}{TOKEN["expiresOn"]}{quote}',
    ]


@pytest.mark.parametrize('system,prefix', [('Darwin', 'export '), ('Linux', 'export '), ('Windows', 'set ')])
def test_env_mode_platform_default(monkeypatch, system, prefix):
    monkeypatch.setattr(temp_token_env.platform, 'system', lambda: system)
    lines = temp_token_env_lines(TOKEN, tenant_url=TENANT_URL, mode='env')
    assert all(line.startswith(prefix) for line in lines)
