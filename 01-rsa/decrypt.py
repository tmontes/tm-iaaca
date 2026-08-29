import base64
import pathlib
import sys

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


def load_private_key(filename, password, encoding='UTF-8'):
    private_key_bytes = pathlib.Path(filename).read_bytes()
    if password is not None:
        password = password.decode(encoding)
    return serialization.load_pem_private_key(private_key_bytes, password)


def decrypt(private_key, ciphertext, encoding='UTF-8'):
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode(encoding)
 

def binary_from_stdin():
    prompt = 'Base64 ciphertext: ' if sys.stdin.isatty() else ''
    base64_text = input(prompt)
    base64_bytes = base64_text.encode('ASCII')
    return base64.b64decode(base64_bytes)


def text_to_stdout(text):
    print(text)



if __name__ == '__main__':

    def cli_args(command=sys.argv[0], args=sys.argv[1:]):
        match args:
            case (private_key_filename,):
                return private_key_filename, None
            case (private_key_filename, key_password):
                return private_key_filename, key_password
            case _:
                raise SystemExit(f'Usage: {command} PRIVATE_KEY [KEY_PASSWORD]')

    private_key_filename, key_password = cli_args()
    private_key = load_private_key(private_key_filename, key_password)
    cyphertext = binary_from_stdin()
    plaintext = decrypt(private_key, cyphertext)
    text_to_stdout(plaintext)
