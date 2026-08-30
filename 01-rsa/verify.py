import sys

from lib import rsa_compute as compute
from lib import rsa_io as io
from lib import std_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (public_key_filename,):
            return public_key_filename
        case _:
            raise SystemExit(f'Usage: {command} PUBLIC_KEY')


if __name__ == '__main__':

    public_key_filename = cli_args()
    public_key = io.load_public_key(public_key_filename)
    message = std_io.read_text(prompt='Message to verify: ')
    signature = std_io.read_binary(prompt='Base64 signature: ')
    verified = compute.verify(public_key, message, signature)
    std_io.write_text(verified, lead='Verified: ')
