# Trust Me, I'm a Certificate Authority

*A hands-on introduction to RSA, X.509, certificate authorities, TLS and interception — in Python.*

Workshop material for PyCon PT 2026.

## DISCLAIMER

**THIS IS TEACHING MATERIAL, NOT SECURITY SOFTWARE.**

* IT CUTS CORNERS ON PURPOSE AND SEVERAL EXERCISES ARE DELIBERATELY BROKEN.
* REAL SECURITY IS A GREAT DEAL MORE THAN THIS.
* USE NONE OF IT FOR ANYTHING THAT MATTERS, AND NEVER TRUST A CA YOU BUILT HERE.


## What this is

Six chapters of exercises in which you build a miniature public-key infrastructure yourself:
RSA key pairs, signatures, X.509 certificates, your own certificate authority, a real HTTPS
server with a real client that refuses to trust it — and then an interception attack that
succeeds anyway.

One question runs through all of it:

> **Alice** wants to talk to **Bob**. **Eve** wants to listen.
> How can **Alice** know she is really talking to **Bob**?

You write the scripts. Each chapter gives you the support modules to build them from, a
`README.md` with the exercises, and occasionally a finished tool to point at your own work.
The code is deliberately small, readable, composable at the shell — and breakable on purpose.
None of it is fit for production, and several exercises exist only to show you why.


## Requirements and preparation

Python **3.12 or newer** (3.12, 3.13 and 3.14 are all fine) and four packages:
`cryptography`, `flask`, `hypercorn`, `requests`.

**Do this before the workshop starts.** It is the one part of the day that cannot be hurried,
and a laptop that installs nothing at minute five costs you a chapter.

### With uv

```console
$ uv sync
```

Then prefix commands with `uv run`:

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

The chapter READMEs are written the second way — `python …`, `hypercorn …`. If you use `uv`,
read those as `uv run python …` and `uv run hypercorn …`.

### Check it works

```console
$ cd 01-rsa
$ python generate_keypair.py smoketest
WARNING: Private key not encrypted!
Created file 'smoketest-private.pem'.
Created file 'smoketest-public.pem'.
```

That exercises Python, `cryptography` and the given modules together. Delete the two files
afterwards and you are ready. A `ModuleNotFoundError` means the environment is not active, or the
packages are not installed in it; a `SyntaxError` means your Python is too old — check `python -V`.


## Layout

One directory per chapter, worked in order:

| Chapter | Subject |
|---|---|
| `01-rsa/` | keys, encryption, signatures |
| `02-certificates/` | X.509 — binding a key to an identity |
| `03-ca/` | becoming a certificate authority |
| `04-tls/` | real HTTPS, with a client that checks |
| `05-mitm/` | interception, and where trust actually lives |
| `06-broken/` | certificates that fail, and which check caught them |

Each chapter directory is **self-contained** — everything it needs is inside it, so you can
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
└── …                      your own scripts go here
```

**`lib/` accumulates.** Chapter 1 has `std_io` and the `rsa_*` pair; chapter 2 adds `x509_*`;
chapter 3 adds `ca_*`; chapters 4 to 6 carry all of them. Import them as
`from lib import rsa_compute as compute`.

**Tools you are given**, beyond `lib/`:

* `generate_keypair.py` — in every chapter. Read it first: it is the shape all your scripts take.
* `webapp.py` — chapters 4 to 6. A minimal Flask application to serve over TLS.
* `tcp_proxy.py` and `tls_proxy.py` — chapter 5. **Eve**'s tools.

**Your scripts live at the chapter root**, next to `lib/`, and you run them from there — they
read and write files in the current directory. Later chapters reuse what you wrote earlier, so
copy those scripts across as you go, along with any `*.pem` files you want to keep. Each
chapter's README opens by saying what to bring.

Every key and certificate you make is yours and stays out of version control: `*.pem` is
ignored by git.
