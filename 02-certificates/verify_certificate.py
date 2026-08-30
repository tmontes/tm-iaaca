import sys

from lib import rsa_io
from lib import std_io
from lib import x509_compute as compute
from lib import x509_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (certificate_filename, public_key_filename):
            return certificate_filename, public_key_filename
        case _:
            raise SystemExit(f'Usage: {command} CERTIFICATE PUBLIC_KEY')


if __name__ == '__main__':

    certificate_filename, public_key_filename = cli_args()
    certificate = io.load_certificate(certificate_filename)
    public_key = rsa_io.load_public_key(public_key_filename)
    verified = compute.verify_certificate_signature(public_key, certificate)
    std_io.write_text(verified, lead='Verified: ')
