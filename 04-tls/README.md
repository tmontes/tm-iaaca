# Real HTTPS (HTTP over TLS)

The `webapp.py` beside this README is given: a minimal Flask application.
It is served by `hypercorn`, which speaks TLS directly.
`generate_keypair.py` is beside it, as always.
`lib/` gains nothing this chapter; everything you need is already there.

Bring your `create_ca.py`, `issue_certificate.py` and `inspect_certificate.py` along,
then set up `workshop-ca` and a key pair for `bob`.

Every certificate so far has been checked by hand. Now a TLS client does it,
and it is far less forgiving than you were.


## 1. Bob Serves HTTP

Launch the application with no encryption at all:

```console
$ hypercorn --bind localhost:8000 webapp:app
```

It holds the terminal while it runs — leave it there, and use a second one for **Alice**.

* Create a `fetch.py` script:
  fetches a given URL with `requests.get` and reports the status and body it got back.

* Point it at `http://localhost:8000`. It answers immediately.

* No keys, no certificate, no CA, nobody's permission.
  What has **Alice** learnt about who answered — and who else has read it?


## 2. A Certificate for a Host

* Create an `issue_server_certificate.py` script:
  like your `issue_certificate.py`, except it also hands the host names the certificate
  should cover to `ca_compute.issue_certificate` as its `dns_names` argument —
  a sequence of names, even when there is only one.

* Use it to issue **Bob** a certificate for `localhost`.
  It covers the same key as before, so it needs a name of its own — the host's.

* Inspect both certificates. Apart from a new serial number and timestamps,
  `inspect_certificate.py` shows no difference at all.
  Whatever you just added, it cannot see.


## 3. Bob Serves HTTPS

Stop the HTTP server with CTRL-C and launch it again, now with **Bob**'s
certificate and private key (add `--keyfile-password` if his key is encrypted):

```console
$ hypercorn --bind localhost:8443 --certfile CERTIFICATE --keyfile PRIVATE_KEY webapp:app
```

* The certificate is public — **Bob** hands it to anyone who connects.
  So why does the server need his *private* key as well?

* Point `fetch.py` at `https://localhost:8443`.
  It fails, where plain HTTP never did.

* This attempt was encrypted and the first one was not.
  So what exactly is the client refusing?

* Teach `fetch.py` whom to trust: pass the CA certificate to `requests.get`
  as its `verify` argument. Ask again.

Then break it:

* Serve the certificate your `issue_certificate.py` makes for `localhost`.
  Trusted CA, right name in the subject, not expired — refused anyway.
  Which part of the certificate was the client actually reading?

* `requests.get` also accepts `verify=False`. Give `fetch.py` a way to ask for that,
  then try it and read what `requests` says about it.
  What is left of HTTPS then, and what is gone?


## 4. Parting Thoughts

**Alice** reached **Bob** over plain HTTP without asking anyone's permission.
Over HTTPS she was refused — and that was the encrypted attempt.

Between the refusal and the success, the certificate did not change.
Neither did the server, nor the encryption.
What changed was the one file **Alice** chose to trust.

That file is now the only thing standing between her and **Eve**.
