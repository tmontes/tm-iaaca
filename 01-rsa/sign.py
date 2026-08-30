import sys

from lib import rsa_compute as compute
from lib import rsa_io as io
from lib import std_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (private_key_filename,):
            return private_key_filename, None
        case (private_key_filename, key_password):
            return private_key_filename, key_password
        case _:
            raise SystemExit(f'Usage: {command} PRIVATE_KEY [KEY_PASSWORD]')


if __name__ == '__main__':

    private_key_filename, key_password = cli_args()
    private_key = io.load_private_key(private_key_filename, key_password)
    message = std_io.read_text(prompt='Message to sign: ')
    signature = compute.sign(private_key, message)
    std_io.write_binary(signature, lead='Base64 signature: ')
