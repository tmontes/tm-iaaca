import base64
import pathlib
import sys

from cryptography.hazmat.primitives import serialization

import rsa_compute as rsa


def _save_bytes(payload, *, filename):
    try:
        with open(filename, 'xb') as f:
            f.write(payload)
    except FileExistsError:
        raise SystemExit(f'Will not overwrite existing file {filename!r}.')
    print(f'Created file {filename!r}.')


def save_private_key(private_key, key_name, key_password, *, name_suffix='-private'):
    private_key_bytes = rsa.get_private_bytes(private_key, key_password=key_password)
    _save_bytes(private_key_bytes, filename=f'{key_name}{name_suffix}.pem')


def save_public_key(private_key, key_name, *, name_suffix='-public'):
    public_key_bytes = rsa.get_public_bytes(private_key)
    _save_bytes(public_key_bytes, filename=f'{key_name}{name_suffix}.pem')


def load_public_key(filename):
    public_key_bytes = pathlib.Path(filename).read_bytes()
    return serialization.load_pem_public_key(public_key_bytes)


def load_private_key(filename, key_password, encoding='UTF-8'):
    private_key_bytes = pathlib.Path(filename).read_bytes()
    if key_password is not None:
        key_password = key_password.decode(encoding)
    return serialization.load_pem_private_key(private_key_bytes, key_password)


def text_from_stdin(*, prompt):
    prompt = prompt if sys.stdin.isatty() else ''
    return input(prompt)


def text_to_stdout(text, *, lead):
    if sys.stdout.isatty():
        print(lead, end='')
    print(text)


def binary_from_stdin(*, prompt):
    prompt = prompt if sys.stdin.isatty() else ''
    base64_text = input(prompt)
    base64_bytes = base64_text.encode('ASCII')
    return base64.b64decode(base64_bytes)


def binary_to_stdout(payload, *, lead):
    if sys.stdout.isatty():
        print(lead, end='')
    base64_bytes = base64.b64encode(payload)
    base64_text = base64_bytes.decode('ASCII')
    print(base64_text)
