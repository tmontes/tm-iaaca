import sys

from lib import rsa_compute as compute
from lib import rsa_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (key_name,):
            return key_name, None
        case (key_name, key_password):
            return key_name, key_password
        case _:
            raise SystemExit(f'Usage: {command} KEY_NAME [KEY_PASSWORD]')


if __name__ == '__main__':

    key_name, key_password = cli_args()
    private_key = compute.generate_private_key()
    io.save_private_key(private_key, key_name, key_password)
    io.save_public_key(private_key, key_name)
