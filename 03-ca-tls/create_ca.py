import sys

from lib import ca_compute as compute
from lib import rsa_compute
from lib import rsa_io
from lib import x509_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (ca_name,):
            return ca_name, None
        case (ca_name, key_password):
            return ca_name, key_password
        case _:
            raise SystemExit(f'Usage: {command} CA_NAME [KEY_PASSWORD]')


if __name__ == '__main__':

    ca_name, key_password = cli_args()
    private_key = rsa_compute.generate_private_key()
    rsa_io.save_private_key(private_key, ca_name, key_password)
    certificate = compute.create_ca_certificate(private_key, ca_name)
    x509_io.save_certificate(certificate, ca_name)
