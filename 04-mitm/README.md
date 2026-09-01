# The Man in the Middle

Given beside this README: the same `webapp.py`, `generate_keypair.py`, `create_csr.py`
and `create_server_csr.py` as before, a `tcp_proxy.py` that relays bytes and shows you
every one of them, and a `tls_proxy.py` that speaks TLS to both ends and prints what it
finds in between.
`lib/` gains nothing.

Bring your `create_ca.py`, `issue_certificate.py` and `fetch.py` along.
Then set up `workshop-ca`, key pairs for `bob` and `eve`,
and issue **Bob** a certificate for `localhost`.

**Alice** trusts `workshop-ca`. Only `workshop-ca`.

This is the diagram from the first ten minutes, finally built:
**Alice**, then **Eve**, then **Bob**. You will want a terminal for each.


## 1. Eve Listens

Serve the application with no encryption, and put the wiretap in front of it —
each in its own terminal:

```console
$ hypercorn --bind localhost:8000 webapp:app
$ python tcp_proxy.py 9000 8000
```

* Point `fetch.py` at `http://localhost:9000`, then read **Eve**'s terminal.
  How much of the conversation does she have?

Stop both with CTRL-C, then serve the same application over TLS
and relay that instead:

```console
$ hypercorn --bind localhost:8443 --certfile CERTIFICATE --keyfile PRIVATE_KEY webapp:app
$ python tcp_proxy.py 9000 8443
```

* Fetch `https://localhost:9000`, trusting `workshop-ca`. It works.
  **Eve** sat in the middle of that connection and it still worked. Why?

* Read her output again. The conversation is gone, but one thing is still legible —
  look at the very first thing **Alice** sends. Why would TLS send that in the clear?

* **Eve** has every byte and cannot read a word of it.
  What did listening get her, and what will she have to do instead?


## 2. Eve Speaks

Leave **Bob** serving on 8443, and stop the wiretap — **Eve** is done listening.

* Have **Eve** set up a CA of her own — `totally-legit-ca`, as in the previous chapter —
  and issue herself a certificate for `localhost`.

* Put her in front of **Bob**, presenting that certificate:

```console
$ python tls_proxy.py 9443 8443 CERTIFICATE PRIVATE_KEY
```

* She announces that she will not be checking **Bob**'s certificate.
  Why does that cost her nothing?

* Point `fetch.py` at `https://localhost:9443`, trusting `workshop-ca`. Refused.

* **Eve** speaks TLS, holds a private key, and answers for `localhost` —
  everything **Bob** has. What is she missing?


## 3. Eve Is Trusted

* Ask again, trusting **Eve**'s CA this time. Then read her terminal.
  What is she reading now that the wiretap in section 1 could not?

* **Bob** did not change. His certificate did not change. The encryption did not change.
  What changed?

* Try `--no-ca-check` as well. Compare how much **Alice** had to get wrong
  for each of these to succeed.

Then break it:

* Have `workshop-ca` — the CA **Alice** trusts — issue **Eve** a certificate
  for `localhost`. Stop **Eve** with CTRL-C and start her again presenting that one.

* **Alice** trusts `workshop-ca`, and only `workshop-ca`. She checks everything.
  She is intercepted anyway. Whose mistake was it?


## 4. Parting Thoughts

In that last exercise **Alice** did nothing wrong.
She checked the issuer, the signature, the host name and the dates, and all four were fine.
Next chapter, each of those four fails in turn — and not one of them fails like this.

Encryption was never what failed — **Eve** was inside the encryption every time.
What decided each outcome was who had been vouched for, and by whom.

A CA you trust can vouch for anybody.
That is the whole of what PKI gives you, and the whole of what it costs.
