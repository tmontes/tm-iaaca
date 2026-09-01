import datetime

from cryptography import exceptions, x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509.oid import NameOID


def create_self_signed_certificate(private_key, subject_name, *, valid_from=None, valid_seconds=7200):
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
        .sign(private_key, hashes.SHA256())
    )


def get_subject(certificate):
    return certificate.subject.rfc4514_string()


def get_issuer(certificate):
    return certificate.issuer.rfc4514_string()


def get_serial_number(certificate):
    return certificate.serial_number


def get_valid_from(certificate):
    return certificate.not_valid_before_utc


def get_valid_until(certificate):
    return certificate.not_valid_after_utc


def get_dns_names(certificate):
    try:
        extension = certificate.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    except x509.ExtensionNotFound:
        return []
    return extension.value.get_values_for_type(x509.DNSName)


def get_certificate_bytes(certificate):
    return certificate.public_bytes(encoding=serialization.Encoding.PEM)


def get_public_key(certificate):
    return certificate.public_key()


def get_public_key_pem_bytes(certificate):
    return certificate.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def verify_certificate_signature(public_key, certificate):
    try:
        public_key.verify(
            certificate.signature,
            certificate.tbs_certificate_bytes,
            padding.PKCS1v15(),
            certificate.signature_hash_algorithm
        )
    except exceptions.InvalidSignature:
        return False
    return True
