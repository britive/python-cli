import json
import time

import click
import jwt
import pytest

from pybritive.britive_cli import BritiveCli
from pybritive.helpers import clipboard, token_printer
from pybritive.helpers.token_printer import TempTokenPrinter, decode_token

TENANT_URL = 'https://example.britive-app.com'
KEY = 'pybritive-test-signing-key-0123456789abcdef'


class StubCli:
    print = BritiveCli.print

    def __init__(self, output_format='json'):
        self.output_format = output_format
        self.silent = False
        self.list_separator = '|'


def make_token():
    now = int(time.time())
    access_token = jwt.encode(
        {'sub': 'user-1', 'email': 'user@example.com', 'iat': now, 'exp': now + 3600}, KEY, algorithm='HS256'
    )
    return {'accessToken': access_token, 'expiresOn': '2030-01-01T00:00:00.000Z'}


def run_printer(mode, output_format='json', silent=False, token=None):
    token = token or make_token()
    TempTokenPrinter(mode=mode, token=token, tenant_url=TENANT_URL, silent=silent, cli=StubCli(output_format)).print()
    return token


def test_default_mode_is_json(capsys):
    token = run_printer(None)
    assert json.loads(capsys.readouterr().out) == token


def test_token_mode(capsys):
    token = run_printer('token')
    assert capsys.readouterr().out == f'{token["accessToken"]}\n'


def test_decode_mode_json(capsys):
    run_printer('decode')
    decoded = json.loads(capsys.readouterr().out)
    assert decoded['header']['alg'] == 'HS256'
    assert decoded['payload']['email'] == 'user@example.com'
    assert set(decoded['times']) == {'issued', 'expires', 'expiresIn'}
    assert decoded['times']['expiresIn'] in ('59m', '1h0m')


def test_decode_mode_table_is_flat(capsys):
    run_printer('decode', output_format='table')
    output = capsys.readouterr().out
    assert 'email' in output
    assert 'expiresIn' in output
    assert 'header' not in output


def test_decode_invalid_token():
    with pytest.raises(click.ClickException):
        decode_token('not-a-jwt')


def test_remaining_expired():
    assert token_printer._remaining(-1) == 'expired'
    assert token_printer._remaining(5400) == '1h30m'


@pytest.mark.parametrize(
    'mode,prefix,quote',
    [('env-nix', 'export ', '"'), ('env-winps', '$Env:', '"'), ('env-wincmd', 'set ', '')],
)
def test_env_modes(capsys, mode, prefix, quote):
    token = run_printer(mode)
    assert capsys.readouterr().out.splitlines() == [
        f'{prefix}BRITIVE_TENANT={quote}{TENANT_URL}{quote}',
        f'{prefix}BRITIVE_TOKEN={quote}{token["accessToken"]}{quote}',
        f'{prefix}BRITIVE_TOKEN_EXPIRATION={quote}{token["expiresOn"]}{quote}',
    ]


@pytest.mark.parametrize('system,prefix', [('Darwin', 'export '), ('Linux', 'export '), ('Windows', 'set ')])
def test_env_mode_platform_default(capsys, monkeypatch, system, prefix):
    monkeypatch.setattr(token_printer.platform, 'system', lambda: system)
    run_printer('env')
    assert capsys.readouterr().out.startswith(f'{prefix}BRITIVE_TENANT=')


def patch_clipboard(monkeypatch, system, available):
    calls = []
    monkeypatch.setattr(clipboard.platform, 'system', lambda: system)
    monkeypatch.setattr(clipboard.shutil, 'which', lambda cmd: cmd if cmd in available else None)
    monkeypatch.setattr(clipboard.subprocess, 'run', lambda cmd, **kwargs: calls.append((cmd, kwargs['input'])))
    return calls


@pytest.mark.parametrize(
    'system,available,expected',
    [
        ('Darwin', ['pbcopy'], ['pbcopy']),
        ('Windows', ['clip'], ['clip']),
        ('Linux', ['xclip', 'xsel'], ['xclip', '-selection', 'clipboard']),
    ],
)
def test_clipboard_mode(capsys, monkeypatch, system, available, expected):
    calls = patch_clipboard(monkeypatch, system, available)
    token = run_printer('clipboard')
    assert calls == [(expected, token['accessToken'])]
    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'copied to clipboard' in captured.err


def test_clipboard_mode_silent(capsys, monkeypatch):
    patch_clipboard(monkeypatch, 'Darwin', ['pbcopy'])
    run_printer('clipboard', silent=True)
    assert capsys.readouterr().err == ''


def test_clipboard_unavailable(monkeypatch):
    patch_clipboard(monkeypatch, 'Linux', [])
    with pytest.raises(click.ClickException, match='No clipboard utility found'):
        run_printer('clipboard')
