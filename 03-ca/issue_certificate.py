import sys

from lib import ca_compute as compute
from lib import ca_io as io
from lib import rsa_io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (subject_name, public_key_filename, ca_private_key_filename):
            return subject_name, public_key_filename, ca_private_key_filename, None
        case (subject_name, public_key_filename, ca_private_key_filename, ca_key_password):
            return subject_name, public_key_filename, ca_private_key_filename, ca_key_password
        case _:
            raise SystemExit(f'Usage: {command} SUBJECT_NAME PUBLIC_KEY CA_PRIVATE_KEY [CA_KEY_PASSWORD]')


if __name__ == '__main__':

    subject_name, public_key_filename, ca_private_key_filename, ca_key_password = cli_args()
    public_key = rsa_io.load_public_key(public_key_filename)
    ca_private_key = rsa_io.load_private_key(ca_private_key_filename, ca_key_password)
    ca_certificate = io.load_ca_certificate(ca_private_key_filename)
    certificate = compute.issue_certificate(ca_private_key, ca_certificate, subject_name, public_key)
    io.save_issued_certificate(certificate, ca_private_key_filename, public_key_filename)
