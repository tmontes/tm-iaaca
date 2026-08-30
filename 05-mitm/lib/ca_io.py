from . import x509_io


def load_ca_certificate(ca_key_filename, *, name_suffix='-certificate'):
    ca_name = x509_io.key_name(ca_key_filename)
    filename = f'{ca_name}{name_suffix}.pem'
    try:
        return x509_io.load_certificate(filename)
    except FileNotFoundError:
        raise SystemExit(f'No certificate {filename!r} found for CA key {ca_key_filename!r}.')


def save_issued_certificate(certificate, ca_key_filename, subject_key_filename):
    ca_name = x509_io.key_name(ca_key_filename)
    subject_name = x509_io.key_name(subject_key_filename, name_suffix='-public')
    x509_io.save_certificate(certificate, f'{ca_name}-{subject_name}')
