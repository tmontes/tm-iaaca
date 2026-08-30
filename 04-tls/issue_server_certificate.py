import sys

from lib import ca_compute
from lib import ca_io
from lib import rsa_io
from lib import x509_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (hostname, public_key_filename, ca_private_key_filename):
            return hostname, public_key_filename, ca_private_key_filename, None
        case (hostname, public_key_filename, ca_private_key_filename, ca_key_password):
            return hostname, public_key_filename, ca_private_key_filename, ca_key_password
        case _:
            raise SystemExit(f'Usage: {command} HOSTNAME PUBLIC_KEY CA_PRIVATE_KEY [CA_KEY_PASSWORD]')


if __name__ == '__main__':

    hostname, public_key_filename, ca_private_key_filename, ca_key_password = cli_args()
    public_key = rsa_io.load_public_key(public_key_filename)
    ca_private_key = rsa_io.load_private_key(ca_private_key_filename, ca_key_password)
    ca_certificate = ca_io.load_ca_certificate(ca_private_key_filename)
    certificate = ca_compute.issue_certificate(
        ca_private_key, ca_certificate, hostname, public_key, dns_names=(hostname,)
    )
    ca_name = x509_io.key_name(ca_private_key_filename)
    holder_name = x509_io.key_name(public_key_filename, name_suffix='-public')
    x509_io.save_certificate(certificate, f'{ca_name}-{holder_name}-{hostname}')
