import sys

from lib import ca_compute as compute
from lib import ca_io as io
from lib import rsa_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (subject_name, csr_filename, ca_private_key_filename):
            return subject_name, csr_filename, ca_private_key_filename, None
        case (subject_name, csr_filename, ca_private_key_filename, ca_key_password):
            return subject_name, csr_filename, ca_private_key_filename, ca_key_password
        case _:
            raise SystemExit(f'Usage: {command} SUBJECT_NAME REQUEST CA_PRIVATE_KEY [CA_KEY_PASSWORD]')


if __name__ == '__main__':

    subject_name, csr_filename, ca_private_key_filename, ca_key_password = cli_args()
    csr = io.load_csr(csr_filename)
    if not compute.verify_csr_signature(csr):
        raise SystemExit(f'Certificate request {csr_filename!r} is not correctly signed.')
    ca_private_key = rsa_io.load_private_key(ca_private_key_filename, ca_key_password)
    ca_certificate = io.load_ca_certificate(ca_private_key_filename)
    certificate = compute.issue_certificate(ca_private_key, ca_certificate, subject_name, csr)
    io.save_issued_certificate(certificate, ca_private_key_filename, csr_filename)
