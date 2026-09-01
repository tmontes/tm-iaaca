import sys

from lib import ca_compute as compute
from lib import ca_io as io
from lib import rsa_io
from lib import x509_io


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
    csr = compute.create_csr(private_key, subject_name)
    io.save_csr(csr, x509_io.key_name(private_key_filename))
