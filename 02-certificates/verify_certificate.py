import sys

from lib import std_io
from lib import x509_compute as compute
from lib import x509_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (certificate_filename, issuer_certificate_filename):
            return certificate_filename, issuer_certificate_filename
        case _:
            raise SystemExit(f'Usage: {command} CERTIFICATE ISSUER_CERTIFICATE')


if __name__ == '__main__':

    certificate_filename, issuer_certificate_filename = cli_args()
    certificate = io.load_certificate(certificate_filename)
    issuer_certificate = io.load_certificate(issuer_certificate_filename)
    issuer_public_key = compute.get_public_key(issuer_certificate)
    verified = compute.verify_certificate_signature(issuer_public_key, certificate)
    std_io.write_text(verified, lead='Verified: ')
