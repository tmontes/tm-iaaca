# Break the PKI

Nothing new is given here, and `lib/` gains nothing —
though it has been hiding something you have not used yet.

Bring your `create_ca.py`, `issue_certificate.py`, `fetch.py`
and `inspect_certificate.py` along, with the `create_private_key.py`, `webapp.py`,
`create_csr.py` and `create_server_csr.py` you were given earlier.
Set up `workshop-ca`, `evil-ca`, and a key pair for `bob`.

**Alice** trusts `workshop-ca`, and nothing else, for the whole of this chapter.
**Bob** serves on 8443:

```console
$ hypercorn --bind localhost:8443 --certfile CERTIFICATE --keyfile PRIVATE_KEY webapp:app
```

No new scripts here. Only certificates that do not work, and the question of why.


## 1. Sharpen Your Tools (optional)

* `x509_compute` has a `get_dns_names` you have never called.
  Teach `inspect_certificate.py` to print what it returns.

* Run it over every certificate you have made so far.
  Which of them name a host at all?


## 2. Four Certificates That Fail

Serve each of these to **Alice** in turn. For each one, predict the error
before you run it, then read what she actually says.

* One issued by `evil-ca` for `localhost`.

* One issued by `workshop-ca` for `bob.local`.

* One issued by `workshop-ca` from a request that never mentioned `localhost` —
  the plain `create_csr.py`, not the server one.

* One issued by `workshop-ca` for `localhost` that expired an hour ago.
  None of your scripts can do that. Use the library from the REPL
  and move `valid_from` into the past.

Then sort them out:

* Two of those four fail with the *same* message, for entirely different reasons.
  Which two, and what would you have to look at to tell them apart?

* One of the four is signed by a CA **Alice** trusts, names the host she asked for,
  and has not expired. Why is it still refused?

* Put them in order, from the mistake easiest to make to the hardest.


## 3. Parting Thoughts

Four broken certificates, four checks that caught them.
The attack in the previous chapter passed all four, and nothing caught it.

So, back to the question from the first ten minutes:
how can **Alice** know she is really talking to **Bob**?

You have built every piece of the answer — keys, signatures, certificates,
an authority, a chain, and a handshake that refuses.
The answer is in none of them.

She believes it because someone she already trusts said so.
That is the whole of PKI, and the hard part was never the mathematics.
