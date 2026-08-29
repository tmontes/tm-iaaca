import sys

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def generate_private_key(*, public_exponent=65537, key_size=2048):
    return rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
    )


def get_private_bytes(private_key, *, key_password, encoding='UTF-8'):
    if key_password is not None:
        ea = serialization.BestAvailableEncryption(key_password.encode(encoding))
    else:
        print('WARNING: Private key not encrypted!', file=sys.stderr)
        ea = serialization.NoEncryption()
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=ea,
    )


def get_public_bytes(private_key):
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def encrypt(public_key, plaintext, *, encoding='UTF-8'):
    return public_key.encrypt(
        plaintext.encode(encoding),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt(private_key, ciphertext, encoding='UTF-8'):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode(encoding)
