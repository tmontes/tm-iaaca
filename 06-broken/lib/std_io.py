import base64
import sys


def read_text(*, prompt):
    prompt = prompt if sys.stdin.isatty() else ''
    return input(prompt)


def write_text(text, *, lead):
    if sys.stdout.isatty():
        print(lead, end='')
    print(text)


def read_binary(*, prompt):
    prompt = prompt if sys.stdin.isatty() else ''
    base64_text = input(prompt)
    base64_bytes = base64_text.encode('ASCII')
    return base64.b64decode(base64_bytes)


def write_binary(payload, *, lead):
    if sys.stdout.isatty():
        print(lead, end='')
    base64_bytes = base64.b64encode(payload)
    base64_text = base64_bytes.decode('ASCII')
    print(base64_text)


def write_pem(pem_bytes, *, lead):
    if sys.stdout.isatty():
        print(f'\n{lead}')
    print(pem_bytes.decode('ASCII'), end='')
