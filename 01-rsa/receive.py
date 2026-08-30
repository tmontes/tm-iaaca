import sys

import rsa_compute as compute
import rsa_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (public_key_filename, private_key_filename):
            return public_key_filename, private_key_filename, None
        case (public_key_filename, private_key_filename, key_password):
            return public_key_filename, private_key_filename, key_password
        case _:
            raise SystemExit(f'Usage: {command} PUBLIC_KEY PRIVATE_KEY [KEY_PASSWORD]')


if __name__ == '__main__':

    public_key_filename, private_key_filename, key_password = cli_args()
    public_key = io.load_public_key(public_key_filename)
    private_key = io.load_private_key(private_key_filename, key_password)
    cyphertext = io.binary_from_stdin(prompt='Base64 ciphertext: ')
    signature = io.binary_from_stdin(prompt='Base64 signature: ')
    message = compute.decrypt(private_key, cyphertext)
    verified = compute.verify(public_key, message, signature)
    io.text_to_stdout(message, lead='Message received: ')
    io.text_to_stdout(verified, lead='Verified: ')
