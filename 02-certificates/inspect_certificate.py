import sys

from lib import std_io
from lib import x509_compute as compute
from lib import x509_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (certificate_filename,):
            return certificate_filename
        case _:
            raise SystemExit(f'Usage: {command} CERTIFICATE')


if __name__ == '__main__':

    certificate_filename = cli_args()
    certificate = io.load_certificate(certificate_filename)
    std_io.write_text(compute.get_subject(certificate), lead='Subject: ')
    std_io.write_text(compute.get_issuer(certificate), lead='Issuer: ')
    std_io.write_text(compute.get_serial_number(certificate), lead='Serial number: ')
    std_io.write_text(compute.get_valid_from(certificate), lead='Valid from: ')
    std_io.write_text(compute.get_valid_until(certificate), lead='Valid until: ')
    std_io.write_pem(compute.get_certificate_public_bytes(certificate), lead='Public key:')
