# X.509 Certificates

`lib/` gains `x509_compute.py` and `x509_io.py` for this chapter's exercises.
The `rsa_*.py` and `std_io.py` modules came along from the previous chapter, unchanged.

A certificate is a public key and an identity, bundled with a validity period
and a serial number, and *signed*. You already know how to sign things.

You will need a key pair to work with: copy **Bob**'s private key over from the
previous chapter, or make a fresh one with the given `create_private_key.py`.

From here on that is all you need: it writes the private key and nothing else.
A public key no longer travels as a file of its own — a certificate is how it travels now.


## 1. Create a Self-Signed Certificate

* Create a `create_certificate.py` script:
  builds a certificate for a given subject name and key pair,
  signed with that same key.

* Use it to create a certificate for **Bob**.


## 2. Inspect a Certificate

* Create an `inspect_certificate.py` script:
  prints a certificate's subject, issuer, serial number, validity period and public key.

* Run it on **Bob**'s certificate.
  His key pair is a single file on disk, and the public half is not in it.
  Where is the only copy you now have?

* Note what *self-signed* means here:
  `Subject` and `Issuer` name the same party.

* Which of those fields did **Bob** choose himself?


## 3. Verify a Certificate's Signature

* Create a `verify_certificate.py` script:
  checks whether a certificate's signature was made by the holder of a given
  issuer certificate.

* Run it on **Bob**'s certificate, against **Bob**'s certificate.
  *Self-signed* means it answers `Verified: True` — and that you just asked
  a certificate to vouch for itself.

Then break it:

* Create a certificate that expired yesterday.
  What stopped you?

* Generate a key pair for **Eve** and have her create a certificate
  whose subject is `bob`.
  Inspect it next to **Bob**'s own — can you tell which one is genuine?

* Check **Bob**'s certificate against **Eve**'s, and hers against his.
  Both answer `Verified: False`, and each still verifies against itself.
  What has verification actually told you?


## 4. Parting Thoughts

**Bob** issued a certificate saying **Bob** is **Bob**.
Why should **Alice** believe it?

**Eve** just issued the same certificate, and it verifies just as well.

A certificate is a signed claim about a key,
and it is worth no more than whoever signed it.
Having that claim signed by someone **Alice** already trusts
is what a Certificate Authority is for.
