import sys

import rsa_compute as compute
import rsa_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (public_key_filename,):
            return public_key_filename
        case _:
            raise SystemExit(f'Usage: {command} PUBLIC_KEY')


if __name__ == '__main__':

    public_key_filename = cli_args()
    public_key = io.load_public_key(public_key_filename)
    message = io.text_from_stdin(prompt='Message to verify: ')
    signature = io.binary_from_stdin(prompt='Base64 signature: ')
    verified = compute.verify(public_key, message, signature)
    io.text_to_stdout(verified, lead='Verified: ')
