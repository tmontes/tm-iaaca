import pathlib

from cryptography.x509 import load_pem_x509_certificate

from . import x509_compute as x509


def _save_bytes(payload, *, filename):
    try:
        with open(filename, 'xb') as f:
            f.write(payload)
    except FileExistsError:
        raise SystemExit(f'Will not overwrite existing file {filename!r}.')
    print(f'Created file {filename!r}.')


def key_name(key_filename, *, name_suffix='-private'):
    return pathlib.Path(key_filename).stem.removesuffix(name_suffix)


def save_certificate(certificate, certificate_name, *, name_suffix='-certificate'):
    certificate_bytes = x509.get_certificate_bytes(certificate)
    _save_bytes(certificate_bytes, filename=f'{certificate_name}{name_suffix}.pem')


def load_certificate(filename):
    certificate_bytes = pathlib.Path(filename).read_bytes()
    return load_pem_x509_certificate(certificate_bytes)
