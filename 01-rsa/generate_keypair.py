import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_key_pair():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )


def get_private_bytes(key_pair, *, key_password, encoding='UTF-8'):
    if key_password is not None:
        ea = serialization.BestAvailableEncryption(key_password.encode(encoding))
    else:
        print('WARNING: Private key not encrypted!', file=sys.stderr)
        ea = serialization.NoEncryption()
    return key_pair.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=ea,
    )


def get_public_bytes(key_pair):
    return key_pair.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def save_bytes_to_new_file(payload, filename):
    try:
        with open(filename, 'xb') as f:
            f.write(payload)
    except FileExistsError:
        raise SystemExit(f'Will not overwrite existing file {filename!r}.')
    print(f'Created file {filename!r}.')


def save_private_key(key_pair, key_name, key_password):
    private_key_bytes = get_private_bytes(key_pair, key_password=key_password)
    filename = f'{key_name}-private.pem'
    save_bytes_to_new_file(private_key_bytes, filename)


def save_public_key(key_pair, key_name):
    public_key_bytes = get_public_bytes(key_pair)
    filename = f'{key_name}-public.pem'
    save_bytes_to_new_file(public_key_bytes, filename)



if __name__ == '__main__':

    def cli_args(command=sys.argv[0], args=sys.argv[1:]):
        match args:
            case (key_name,):
                return key_name, None
            case (key_name, key_password):
                return key_name, key_password
            case _:
                raise SystemExit(f'Usage: {command} KEY_NAME [KEY_PASSWORD]')

    key_name, key_password = cli_args()
    key_pair = generate_key_pair()
    save_private_key(key_pair, key_name, key_password)
    save_public_key(key_pair, key_name)
