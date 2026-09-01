import pathlib

from cryptography.x509 import load_pem_x509_csr

from . import ca_compute as ca
from . import x509_io


def _save_bytes(payload, *, filename):
    try:
        with open(filename, 'xb') as f:
            f.write(payload)
    except FileExistsError:
        raise SystemExit(f'Will not overwrite existing file {filename!r}.')
    print(f'Created file {filename!r}.')


def save_csr(csr, request_name, *, name_suffix='-request'):
    csr_bytes = ca.get_csr_bytes(csr)
    _save_bytes(csr_bytes, filename=f'{request_name}{name_suffix}.pem')


def load_csr(filename):
    csr_bytes = pathlib.Path(filename).read_bytes()
    try:
        return load_pem_x509_csr(csr_bytes)
    except ValueError as error:
        raise SystemExit(f'Could not load certificate request {filename!r}: {error}')


def load_ca_certificate(ca_key_filename, *, name_suffix='-certificate'):
    ca_name = x509_io.key_name(ca_key_filename)
    filename = f'{ca_name}{name_suffix}.pem'
    try:
        return x509_io.load_certificate(filename)
    except FileNotFoundError:
        raise SystemExit(f'No certificate {filename!r} found for CA key {ca_key_filename!r}.')


def save_issued_certificate(certificate, ca_key_filename, csr_filename):
    ca_name = x509_io.key_name(ca_key_filename)
    request_name = x509_io.key_name(csr_filename, name_suffix='-request')
    x509_io.save_certificate(certificate, f'{ca_name}-{request_name}')
