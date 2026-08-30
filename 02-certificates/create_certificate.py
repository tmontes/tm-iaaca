import sys

from lib import rsa_io
from lib import x509_compute as compute
from lib import x509_io as io


def cli_args(command=sys.argv[0], args=sys.argv[1:]):
    match args:
        case (subject_name, private_key_filename):
            return subject_name, private_key_filename, None
        case (subject_name, private_key_filename, key_password):
            return subject_name, private_key_filename, key_password
        case _:
            raise SystemExit(f'Usage: {command} SUBJECT_NAME PRIVATE_KEY [KEY_PASSWORD]')


if __name__ == '__main__':

    subject_name, private_key_filename, key_password = cli_args()
    private_key = rsa_io.load_private_key(private_key_filename, key_password)
    certificate = compute.create_self_signed_certificate(private_key, subject_name)
    io.save_certificate(certificate, io.key_name(private_key_filename))
