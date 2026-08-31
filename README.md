# Trust Me, I'm a Certificate Authority

*A hands-on intro to RSA, X.509, PKI, TLS and MITM (man-in-the-middle) attacks with Python.*

Workshop material for PyCon PT 2026.

## DISCLAIMER

**THIS IS TEACHING MATERIAL, NOT SECURITY SOFTWARE.**

* IT CUTS CORNERS ON PURPOSE.
* SEVERAL EXERCISES ARE DELIBERATELY BROKEN.
* REAL SECURITY IS A GREAT DEAL MORE THAN THIS.
* USE NONE OF IT FOR ANYTHING THAT MATTERS.
* NEVER TRUST A CA YOU BUILT HERE.


## The workshop

Six chapters of guided exercises in which you build a miniature public-key infrastructure yourself:
RSA key pairs, signatures, X.509 certificates, your own certificate authority, a real HTTPS
server with a real client that refuses to trust it — and then an interception attack that
succeeds anyway.

One question runs through all of it:

> **Alice** wants to talk to **Bob**. **Eve** wants to listen.
> How can **Alice** know she is really talking to **Bob**?
> How can **Alice** ensure **Eve** cannot listen/tamper with her messages to **Bob**?

You write the scripts. Each chapter gives you the support modules to build them from, a
`README.md` with the exercises, and occasionally a finished tool to point at your own work.
The code is deliberately small, readable, composable at the shell - and breakable on purpose.


## Requirements and preparation

Python 3.12 or newer and four packages: `cryptography`, `flask`, `hypercorn`, `requests`.

### With uv

```console
$ uv sync
```

Then activate the environment or prefix commands with `uv run` as in:

```console
$ uv run python generate_keypair.py alice
```

### Without uv

```console
$ python3 -m venv .venv
$ source .venv/bin/activate          # Windows: .venv\Scripts\activate
$ python -m pip install cryptography flask hypercorn requests
```

Then commands are plain:

```console
$ python generate_keypair.py alice
```


### Check it works

```console
$ cd 01-rsa
$ python generate_keypair.py smoketest
WARNING: Private key not encrypted!
Created file 'smoketest-private.pem'.
Created file 'smoketest-public.pem'.
```

That exercises Python, `cryptography` and the given modules together.
Delete the two files and you are ready.


## Layout Details

One directory per chapter, worked in order:

| Chapter | Directory | Subject |
|---|---|---|
| (all) | `slides/` | Supporting slides. |
| RSA | `01-rsa/` | Fundamentals: keys, encryption, signatures. |
| Certificates | `02-certificates/` | X.509, identities, Subjects and Issuers. |
| Build a CA | `03-ca/` | Issue and verify certificates. |
| TLS Trust | `04-tls/` | Connect a Python client to a HTTPS-enabled Flask server. |
| MITM | `05-mitm/` | Intercept the connection and discover why trust matters. |
| Break It | `06-broken/` | Certificates that fail and checks that catch them. |

Each directory is self-contained with everything it needs inside it, so you can
start any chapter from a clean slate:

```
03-ca/
├── README.md              the exercises
├── lib/                   modules you are given
│   ├── std_io.py            reading and writing the terminal
│   ├── rsa_compute.py       keys, encryption, signatures
│   ├── rsa_io.py            loading and saving key files
│   ├── x509_compute.py      building and reading certificates
│   ├── x509_io.py           loading and saving certificate files
│   ├── ca_compute.py        signing certificates as an authority
│   └── ca_io.py             the files an authority keeps
├── generate_keypair.py    a tool you are given
└── ...                    your own scripts go here
```

The `lib/` directory accumulates:
chapter 1 has `std_io` and the `rsa_*` pair;
chapter 2 adds `x509_*`;
chapter 3 adds `ca_*`;
chapters 4 to 6 carry all of them.

Tools you are given, beyond `lib/`:

* `generate_keypair.py` — in every chapter; read it for review and inspiration.
* `webapp.py` — in chapters 4 to 6; a minimal Flask application to serve over TLS/HTTPS.
* `tcp_proxy.py` and `tls_proxy.py` — in chapter 5; **Eve**'s evil tools.

**Your scripts live at the chapter root**, next to `lib/`, and you run them from there; they
read and write files in the current directory. Later chapters reuse what you wrote earlier, so
copy those scripts across as you go, along with any `*.pem` files you want to keep. Each
chapter's README opens by saying what to bring.

Every key and certificate you make is yours and stays out of version control: `*.pem` is
ignored by git.

Enjoy!
