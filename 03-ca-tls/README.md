# A Certificate Authority, and a Real Connection

You are given:

* Two more modules in `lib/`: `ca_compute.py` and `ca_io.py`, for authorities and requests;
  the `x509_*.py`, `rsa_*.py` and `std_io.py` modules came along from the previous chapter,
  unchanged.

* The `webapp.py` script, a minimal Flask application, to be served by `hypercorn`,
  which speaks TLS directly.

* The `create_csr.py` and `create_server_csr.py` scripts, which build
  *certificate signing requests* - the thing a subject sends a CA when it wants a certificate.
  Read them: there is less in a request than you might expect.

Generate a key pair for `bob`.

**Bob** issued his own certificate and it convinced nobody.
Now someone else issues it for him - and then a real TLS client decides what that is worth.


## 1. Bob Serves HTTP

Launch the web application with no encryption at all:

```console
$ hypercorn --bind localhost:8000 webapp:app
```

It holds the terminal while it runs - leave it there, and use a second one for **Alice**.

* Create a `fetch.py` script that
  fetches a given URL with `requests.get` and reports the status and body it got back.

* Point it at `http://localhost:8000`. It answers immediately.

* No keys, no certificate, no CA, nobody's permission.
  What has **Alice** learnt about who answered - and who else has read it?


## 2. Create the Certificate Authority

* Create a `create_ca.py` script that
  generates a private key and a self-signed certificate for it,
  marked as allowed to sign other certificates:
  it should produce two files, one with the private key and another with the certificate.

* Use it to set up `workshop-ca`.

* Inspect the certificate: your `inspect_certificate.py` from the previous chapter
  runs fine from where you wrote it.
  How does it differ from **Bob**'s self-signed certificate, the one you created there -
  and is there anything in it that makes it trustworthy?


## 3. Request and Issue a Certificate

A CA does not invent certificates out of nothing. Someone asks it for one.

* Use the given `create_csr.py` to have **Bob** request a certificate as `bob`.

* **Bob**'s private key never left him, yet the request is signed.
  Signed with what, and what does that prove?

* `ca_compute` will tell you the subject and the host names a request asks for.
  Read one from the REPL. Is there anything in there a CA could *check*?

* Create an `issue_certificate.py` script that
  reads a request, refuses it unless it is correctly signed, then builds a certificate
  for a given subject name carrying the key out of that request - signed with the CA's
  private key, taking the issuer name from the CA's own certificate.

* Use it to issue **Bob** his certificate.

* Inspect it: `Subject` is `CN=bob`, `Issuer` is `CN=workshop-ca`.

* The signature check proved **Bob** holds the key he sent.
  What did it prove about the *name* he asked for?


## 4. Bob Serves HTTPS

Stop the HTTP server with CTRL-C. **Bob** needs a certificate for the *host name*
**Alice** will use in her HTTPS client, not just for his own name.

* Use the given `create_server_csr.py` to have **Bob** request one for `localhost`,
  then issue it with the same `issue_certificate.py` as before.
  The CA needs no new script - the request carries the difference.

* Inspect it beside the first one. Apart from a new serial number and timestamps,
  `inspect_certificate.py` shows no difference at all.
  Whatever the request added, it cannot see.

Launch the application again, now with that certificate and **Bob**'s private key
(add `--keyfile-password` if his key is encrypted):

```console
$ hypercorn --bind localhost:8443 --certfile CERTIFICATE --keyfile PRIVATE_KEY webapp:app
```

* The certificate is public - **Bob** hands it to anyone who connects.
  So why does the server need his *private* key as well?

* Point `fetch.py` at `https://localhost:8443`.
  It fails, where plain HTTP never did.

* This attempt was encrypted and the first one was not.
  So what exactly is the client refusing?

* Teach `fetch.py` whom to trust: pass the CA certificate to `requests.get`
  as its `verify` argument. Ask again.

Then break it:

* Serve the first certificate instead - the one from the plain request with no hostname.
  Trusted CA, right name in the subject, not expired - refused anyway.
  Which part of the certificate was the client actually reading?

* `requests.get` also accepts `verify=False`. Give `fetch.py` a way to ask for that,
  then try it and read what `requests` says about it.
  What is left of HTTPS then, and what is gone?


## 5. Which Certificate Should Alice Trust?

* Have **Eve** set up a CA of her own, `evil-ca`,
  and have it issue her a certificate for `localhost` whose subject is `bob`.

* Inspect it beside **Bob**'s. Both are signed by a CA, both say `Subject: CN=bob`,
  both cover `localhost`, neither has expired.
  Which one should **Alice** trust, and what exactly is she deciding?

* The filenames name their issuer; **Eve** would not be so helpful -
  nor would she call it `evil-ca`.
  Where does the certificate itself say who issued it - and could it lie?

* Serve **Eve**'s certificate and point `fetch.py` at it, still trusting `workshop-ca`.
  Say what the client will do before you run it.

You compared those two by reading them, and your `verify_certificate.py` would still
check either one against a CA's certificate. From here on the client does that for you,
on every single connection, and it is far less forgiving than you were.

Then break it:

* Have `workshop-ca` - the CA **Alice** trusts - issue a certificate for subject `bob`
  from **Eve**'s request, so it carries **Eve**'s key under **Bob**'s name.
  Nothing stops it. What does that tell you about a CA you trust?


## 6. Parting Thoughts

**Alice** reached **Bob** over plain HTTP without asking anyone's permission.
Over HTTPS she was refused - and that was the encrypted attempt.

Between the refusal and the success, the certificate did not change.
Neither did the server, nor the encryption.
What changed was the one file **Alice** chose to trust.

She no longer has to take **Bob**'s word about **Bob**.
She has to take `workshop-ca`'s word about **Bob**.
The question moved rather than vanished - but it moved somewhere useful.
There is now one certificate **Alice** must obtain carefully, once,
and it can vouch for everyone she will ever talk to.

Which also means whoever holds that CA's private key can vouch for anyone at all.

That one file is now all that stands between her and **Eve**.
