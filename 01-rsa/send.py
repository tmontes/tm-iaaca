import sys

from lib import rsa_compute as compute
from lib import rsa_io as io
from lib import std_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (private_key_filename, public_key_filename):
            return private_key_filename, public_key_filename, None
        case (private_key_filename, public_key_filename, key_password):
            return private_key_filename, public_key_filename, key_password
        case _:
            raise SystemExit(f'Usage: {command} PRIVATE_KEY PUBLIC_KEY [KEY_PASSWORD]')


if __name__ == '__main__':

    private_key_filename, public_key_filename, key_password = cli_args()
    private_key = io.load_private_key(private_key_filename, key_password)
    public_key = io.load_public_key(public_key_filename)
    message = std_io.read_text(prompt='Message to send: ')
    signature = compute.sign(private_key, message)
    cyphertext = compute.encrypt(public_key, message)
    std_io.write_binary(cyphertext, lead='Base64 ciphertext: ')
    std_io.write_binary(signature, lead='Base64 signature: ')
