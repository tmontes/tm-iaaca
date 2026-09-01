import datetime

from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.x509.oid import NameOID

# A certificate authority signs certificates, and nothing else.
CA_KEY_USAGE = x509.KeyUsage(
    key_cert_sign=True,
    crl_sign=True,
    digital_signature=False,
    content_commitment=False,
    key_encipherment=False,
    data_encipherment=False,
    key_agreement=False,
    encipher_only=False,
    decipher_only=False,
)


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
        .add_extension(CA_KEY_USAGE, critical=True)
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
                       critical=False)
        .sign(private_key, hashes.SHA256())
    )


def create_csr(private_key, subject_name, *, dns_names=()):
    builder = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject_name)]))
    )
    if dns_names:
        builder = builder.add_extension(
            x509.SubjectAlternativeName([x509.DNSName(name) for name in dns_names]),
            critical=False
        )
    return builder.sign(private_key, hashes.SHA256())


# For reading a request in the REPL: the CA deliberately never calls this.
def get_csr_subject(csr):
    return csr.subject.rfc4514_string()


def get_csr_dns_names(csr):
    try:
        extension = csr.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    except x509.ExtensionNotFound:
        return []
    return extension.value.get_values_for_type(x509.DNSName)


def get_csr_bytes(csr):
    return csr.public_bytes(encoding=serialization.Encoding.PEM)


# A request is signed by the very key it carries: whoever sent it holds that key.
# It says nothing whatsoever about the name being asked for.
def verify_csr_signature(csr):
    return csr.is_signature_valid


def issue_certificate(
    ca_private_key,
    ca_certificate,
    subject_name,
    csr,
    *,
    valid_from=None,
    valid_seconds=7200,
    ca=False,
):
    if valid_from is None:
        valid_from = datetime.datetime.now(datetime.UTC)
    dns_names = get_csr_dns_names(csr)
    builder = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject_name)]))
        .issuer_name(ca_certificate.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(valid_from)
        .not_valid_after(valid_from + datetime.timedelta(seconds=valid_seconds))
        .add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_certificate.public_key()),
            critical=False
        )
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
