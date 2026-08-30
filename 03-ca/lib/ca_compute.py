import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID


def create_ca_certificate(private_key, subject_name, *, valid_from=None, valid_seconds=7200):
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject_name)])
    if valid_from is None:
        valid_from = datetime.datetime.now(datetime.UTC)
    return (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_from + datetime.timedelta(seconds=valid_seconds))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(private_key, hashes.SHA256())
    )


def issue_certificate(
    ca_private_key,
    ca_certificate,
    subject_name,
    public_key,
    *,
    valid_from=None,
    valid_seconds=7200,
    ca=False,
    dns_names=(),
):
    if valid_from is None:
        valid_from = datetime.datetime.now(datetime.UTC)
    builder = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject_name)]))
        .issuer_name(ca_certificate.subject)
        .public_key(public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_from + datetime.timedelta(seconds=valid_seconds))
    )
    if ca:
        builder = builder.add_extension(
            x509.BasicConstraints(ca=True, path_length=None),
            critical=True
        )
    if dns_names:
        builder = builder.add_extension(
            x509.SubjectAlternativeName([x509.DNSName(name) for name in dns_names]),
            critical=False
        )
    return builder.sign(ca_private_key, hashes.SHA256())
