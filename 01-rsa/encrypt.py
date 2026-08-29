import base64
import pathlib
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_public_key(filename):
    public_key_bytes = pathlib.Path(filename).read_bytes()
    return serialization.load_pem_public_key(public_key_bytes)


def encrypt(public_key, plaintext, *, encoding='UTF-8'):
    return public_key.encrypt(
        plaintext.encode(encoding),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
 

def text_from_stdin():
    prompt = 'Plaintext message: ' if sys.stdin.isatty() else ''
    return input(prompt)


def binary_to_stdout(payload):
    base64_bytes = base64.b64encode(payload)
    base64_text = base64_bytes.decode('ASCII')
    print(base64_text)



if __name__ == '__main__':

    def cli_args(command=sys.argv[0], args=sys.argv[1:]):
        match args:
            case (public_key_filename,):
                return public_key_filename
            case _:
                raise SystemExit(f'Usage: {command} PUBLIC_KEY')

    public_key_filename = cli_args()
    plaintext = text_from_stdin()
    public_key = load_public_key(public_key_filename)
    cyphertext = encrypt(public_key, plaintext)
    binary_to_stdout(cyphertext)
