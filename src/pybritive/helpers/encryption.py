import uuid
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import click


class InvalidPassphraseException(Exception):
    pass


class StringEncryption:
    def __init__(self, passphrase: str = None):
        self.passphrase = passphrase or str(uuid.getnode())  # TODO change?

    @staticmethod
    def _salt():
        return base64.b64encode(os.urandom(32)).decode('utf-8')

    def _key(self, salt: str):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=base64.b64decode(salt.encode()),
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(self.passphrase.encode()))

    def encrypt(self, plaintext: str) -> str:
        salt = self._salt()
        key = self._key(salt)
        ciphertext = Fernet(key).encrypt(plaintext.encode('utf-8'))
        return f'{base64.b64encode(ciphertext).decode("utf-8")}:{salt}'

    def decrypt(self, ciphertext: str):
        try:
            ciphertext, b64salt = ciphertext.split(':')
            key = self._key(b64salt)
            return Fernet(key).decrypt(base64.b64decode(ciphertext.encode())).decode('utf-8')
        except InvalidToken:
            raise InvalidPassphraseException()
