import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generateKey(prompt):
    alphabet = r'q!e@p#i$w$o%u^r&t(y)a-h=fl_g]d{j]s}k\v"n;x/c.b,z>m<'
    salt = ""
    for letter in prompt:
        if letter in alphabet:
            salt += alphabet[(alphabet.index(letter) + len(prompt)) % 26]
    salt = bytes(salt[::-1], 'utf8')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32,
                     salt=salt, iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(bytes(prompt, 'utf8')))


def encrypt(key, value):
    cipher_suite = Fernet(key)
    # required to be bytes
    return cipher_suite.encrypt((value).encode('utf-8'))


def decrypt(key, value):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(value).decode('utf-8')


def generateRandomKey():
    return secrets.token_urlsafe(32) + '='
