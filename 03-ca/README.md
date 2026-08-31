# Becoming a Certificate Authority

`lib/` gains `ca_compute.py` and `ca_io.py` for this chapter's exercises.
The `x509_*.py`, `rsa_*.py` and `std_io.py` modules came along from the previous chapter, unchanged.

**Bob** issued his own certificate and it convinced nobody.
Now someone else issues it for him.

Generate key pairs for `bob` and `eve` before you start, with the given `generate_keypair.py`.
The certificate authorities will make their own.


## 1. Create the Certificate Authority

* Create a `create_ca.py` script:
  generates a key pair and a matching self-signed certificate,
  marked as allowed to sign other certificates.

* Use it to set up `workshop-ca`.

* Inspect the certificate. How does it differ from **Bob**'s self-signed certificate
  from the previous chapter — and is there anything in it that makes it trustworthy?


## 2. Issue a Certificate

* Create an `issue_certificate.py` script:
  builds a certificate for a given subject name and *public* key,
  signed with the CA's private key, taking the issuer name from the CA's own certificate.

* Use it to issue a certificate for **Bob**.

* Inspect it: `Subject` is `CN=bob`, `Issuer` is `CN=workshop-ca`.
  Confirm the public key it carries is **Bob**'s.

* **Bob**'s private key was never involved.
  What did the CA actually check before signing?

* Verify its signature with your `verify_certificate.py`, against `workshop-ca`'s public key
  and then against **Bob**'s own.
  Last chapter **Bob**'s key verified **Bob**'s certificate — why not now?

* `workshop-ca`'s public key is also inside its certificate.
  Which copy would a program checking a chain of certificates use?


## 3. Which Certificate Should Alice Trust?

* Have **Eve** set up a CA of her own, `totally-legit-ca`.

* Have her CA issue a certificate whose subject is `bob`,
  carrying **Eve**'s public key.

* Inspect both certificates side by side.
  Both are signed by a CA, both say `Subject: CN=bob`, neither has expired.
  Which one should **Alice** trust, and what exactly is she deciding?

* The filenames name their issuer; **Eve** would not be so helpful.
  Where does the certificate itself say who issued it — and could it lie?

Then break it:

* Have `workshop-ca` — the CA **Alice** trusts — issue a certificate
  for subject `bob` carrying **Eve**'s public key.
  Nothing stops it. What does that tell you about a CA you trust?

* Verify **Eve**'s `bob` certificate against `workshop-ca`'s public key —
  the only CA key **Alice** has. This is the check that saves her.


## 4. Parting Thoughts

**Alice** no longer has to take **Bob**'s word about **Bob**.
She has to take `workshop-ca`'s word about **Bob**.

The question moved rather than vanished - but it moved somewhere useful.
There is now one key **Alice** must obtain carefully, once,
and it can vouch for everyone she will ever talk to.

Which also means whoever holds that CA's private key can vouch for anyone at all.

So far you have been comparing issuers by reading them.
Next, a real TLS connection does the checking for you.
