# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Teaching material for a 2-hour interactive PyCon PT 2026 tutorial: *Trust Me, I'm a Certificate Authority* —
participants build a miniature PKI (RSA → X.509 → CA → TLS → MITM) themselves, in Python.

**The chapter `README.md` files are the spec** for content and sequencing; **`TIMING.md` is the delivery
budget.** There was an `outline.md` holding the original design; it was deleted once the chapters diverged
from it, and it is not coming back — don't reconstruct it.

Deliberately out of scope, and to stay that way: CRLs, OCSP, ACME, intermediate CA hierarchies, TLS
handshake internals, ECC, PEM vs DER details.

The narrative thread is Alice / Bob / Eve and the single question "how can Alice know she's really talking to Bob?".
Code should serve that narrative — small, readable, composable at the shell, and breakable on purpose.

## Layout and status

| Dir | Subject | Status |
|---|---|---|
| `01-rsa/` | RSA fundamentals | implemented |
| `02-certificates/` | X.509 certificates | implemented |
| `03-ca-tls/` | Become a CA, issue from CSRs, then Flask/Hypercorn HTTPS + Requests | implemented |
| `04-mitm/` | MITM and trust anchors | implemented |
| `05-broken/` | Break the PKI, diagnose broken certificates | implemented |

Chapter 3 is a merge of what used to be `03-ca/` and `04-tls/`. They duplicated a full CA setup, a
near-identical second issuing script, and the trust comparison — done by hand in one, by the TLS client in
the other. Merged, the chapter runs problem → build → deploy → break: plain HTTP, create the CA, request
and issue, serve HTTPS, then compare two `CN=bob` certificates. Don't split them back apart.

Each chapter has its own `README.md` — the participant-facing exercise brief (numbered exercises, describing
which scripts *they* write and which support modules are given to them).

## Public keys are not files

`generate_keypair.py` writes a public key file **only in chapter 1**, where certificates do not exist yet and
a bare public key genuinely has to travel between Alice and Bob. From chapter 2 on, a public key lives in
exactly one place: the certificate that carries it. `rsa_io.save_public_key` and `rsa_io.load_public_key`
still exist in every chapter's copy, because `rsa_io.py` stays byte-identical everywhere and only chapter 1
calls them. Don't delete them, and don't reintroduce `-public.pem` anywhere else.

Two consequences that are easy to undo by accident:

* `verify_certificate.py` (chapter 2) takes an **issuer certificate**, not a public key, and reaches the key
  through `x509_compute.get_public_key`.
* `issue_certificate.py` (chapter 3) takes a **certificate signing request**, not a public key.

## Certificates are issued from CSRs

`ca_compute.create_csr` builds the request; `ca_compute.issue_certificate` takes that request and reads both
the public key and the SAN `dns_names` out of it. `issue_certificate` has **no `dns_names` keyword** any
more — a host name gets into a certificate by being in the request, which is why `create_server_csr.py` sits
next to `create_csr.py`. Both are given; participants write the CA's side, not the subject's.

**The CA takes the subject name from its own command line, not from the request.** That asymmetry is
deliberate: it is what lets `workshop-ca` issue a certificate named `bob` from Eve's request, which is
chapter 3's closing break-it drill and the setup for the whole MITM chapter. Don't "fix" it by reading the
subject out of the CSR.

`issue_certificate.py` refuses a request whose signature does not verify. A CSR is signed by the very key it
carries, so that check proves possession of the private key and **nothing about the name** — which is exactly
what the chapter asks immediately afterwards.

The material as built runs ~142 minutes against a 120-minute slot, so **adding an exercise costs something
that is already overdrawn** — check `TIMING.md` before proposing new material, and record the cost there.

## Chapter README style

Terse. `*` bullets, one idea each; a preamble naming what `lib/` gained; numbered `##` sections; a final
`## N. Parting Thoughts` that hands off to the next chapter's question. Sections that can be broken end with
a `Then break it:` list.

- **Say what a script does, never how it is called.** No CLI signatures, no example invocations, no filenames
  — participants design their own interface, and the reference scripts at the chapter root are only one
  possible answer.
- **Prefer questions to statements.** "What did the CA actually check before signing?" beats explaining it.
  The good questions have short, surprising answers ("nothing — you told it to").
- **Bold** for the cast (**Alice**, **Bob**, **Eve**); `code` for subject names and identifiers (`bob`,
  `workshop-ca`). Subject names are single tokens — no spaces to quote at the shell.
- Show what participants will actually see: inspection prints `CN=bob`, so write `CN=bob`.

## Commands

`uv`-managed project, `requires-python >= 3.12`. Dependencies: `cryptography`, `flask`, `hypercorn`, `requests`.
Verified on 3.12.10 (OpenSSL 3.0.16), 3.14.7 (OpenSSL 3.5.7) and 3.15.0rc1 (OpenSSL 3.5.7) — identical
behaviour throughout, including every error message the chapters rely on.

**The server is `hypercorn`, not Waitress** — Waitress cannot do TLS at all, it expects a reverse proxy.
Hypercorn serves the Flask WSGI app directly (no `WSGIMiddleware` needed) and takes `--certfile` /
`--keyfile` / `--keyfile-password`.

**Certificates must carry key identifiers to work over TLS.** OpenSSL 3.5 (shipped with Python 3.14)
enforces RFC 5280 strictly: a chain without `AuthorityKeyIdentifier` fails with *Missing Authority Key
Identifier*, and a CA certificate without `KeyUsage` fails with *CA cert does not include key usage
extension*. Hence `ca_compute` adds `SubjectKeyIdentifier` + critical `KeyUsage(key_cert_sign, crl_sign)`
to CA certificates and `AuthorityKeyIdentifier` to every issued certificate. Manual signature checks pass
without these; TLS does not. OpenSSL 3.0 (Python 3.12) is laxer and would accept certificates lacking them —
**do not remove them on that basis**, or the material breaks for anyone on a newer interpreter.

**Everything runs on `localhost` — no `/etc/hosts` edits, no sudo.** A hostname mismatch is demonstrated by
issuing for `bob.local` and connecting to `localhost`.

```bash
uv sync                       # create/refresh .venv from uv.lock
```

Scripts import the given modules from the chapter's `lib/` package (`from lib import rsa_io`), which
resolves because the script's own directory is `sys.path[0]`. **Run them from inside the chapter
directory** — `*.pem` output lands in the cwd:

```bash
cd 01-rsa
uv run python generate_keypair.py alice s3cr3t      # → alice-private.pem, alice-public.pem
echo "hello Bob" | uv run python encrypt.py bob-public.pem | uv run python decrypt.py bob-private.pem pw
uv run python sign.py alice-private.pem pw          # message on stdin → base64 signature on stdout
```

There is no test suite, linter, or formatter configured. Verification is by hand, at the shell, the way
participants will do it.

## The library accumulates across chapters

Each chapter directory is a **self-contained workspace**. Its `lib/` package carries copies of the support
modules from every earlier chapter, plus the new pair it introduces: `02-certificates/lib/` holds
`std_io.py` + `rsa_compute.py` + `rsa_io.py` (verbatim copies) alongside its own `x509_compute.py` +
`x509_io.py`. Chapter 3 adds a `ca_*` pair on top of those, and so on.

**Inside `lib/`, modules import each other relatively** — `rsa_io.py` does `from . import rsa_compute as rsa`,
`x509_io.py` does `from . import x509_compute as x509`. A library module imports a lower layer only when its
own code needs it; no re-exporting on another module's behalf.

**Scripts import each module directly, from wherever the function they need is defined.**
`create_certificate.py` does `from lib import rsa_io` for `load_private_key` next to
`from lib import x509_io as io` for `save_certificate`. The chapter's own topic keeps the short
`compute`/`io` aliases; carried-over modules keep their full name, so provenance is visible at the call
site (`rsa_io.load_private_key(...)`).

Splitting given code into `lib/` keeps the chapter root as the participant's own workspace, and lets someone
who fell behind start any chapter clean. The cost is duplication: **any change to a carried-over module —
fix or addition — must be propagated to every chapter that carries it**, and the copies are expected to stay
byte-identical (`diff` them). Participants carry their own `*.pem` files and their own scripts forward by hand.

A later chapter may extend an earlier module rather than add a new one when that is where the function
belongs: `x509_compute.get_dns_names` exists for chapter 5's optional inspection exercise, because the
script being extended already imports `x509_compute`. Propagate, then `diff`.

Two kinds of file sit at a chapter root, and **only the README distinguishes them**. Each chapter's
preamble names what is **given**: `generate_keypair.py` in every chapter, `create_csr.py` +
`create_server_csr.py` + `webapp.py` in 03–05, the two proxies in 04. Everything else at the root
(`encrypt.py`, `create_certificate.py`, `fetch.py`, …) is a **reference solution** — participants write their
own. Producing the participant copy of a chapter means deleting the solutions and keeping `README.md`,
`lib/`, and the given scripts.

`generate_keypair.py` is given rather than written so the first ten minutes teach the conventions by
reading a complete example. It keeps the chapter-1 `compute`/`io` aliases everywhere, since a given file is
copied verbatim rather than rewritten per chapter. **It is the one given script whose copies are not all
byte-identical:** chapter 1's writes a public key file too, chapters 2–5 write the private key only. The
02–05 copies must stay byte-identical to each other; the CSR scripts and `webapp.py` are byte-identical
across every chapter that carries them.

**Only `lib/` accumulates. Scripts do not.** A chapter root carries just the scripts its own exercises
introduce — `03-ca-tls/` is `create_ca.py` + `issue_certificate.py` + `fetch.py`, nothing else. Never copy an
earlier chapter's script forward: to exercise chapter 3 end to end, run `01-rsa/generate_keypair.py` and
`02-certificates/inspect_certificate.py` from their own directories, which is what a participant does by
hand with their own copies.

## Per-chapter code architecture

`01-rsa/` establishes the pattern every later chapter should follow.

**Three layers, strictly separated:**

1. `<topic>_compute.py` — pure cryptography via the `cryptography` library. Takes and returns key objects,
   `str`, and `bytes`. No file access, no stdio, no `sys.exit`. Keyword-only options with defaults
   (`*, encoding='UTF-8'`). Verification failures are translated into return values, not exceptions
   (`verify()` catches `InvalidSignature` → `False`).
2. `<topic>_io.py` — everything impure: PEM load/save, stdin/stdout. Imports the compute module
   (as `rsa`, from `rsa_io`'s point of view).
3. Thin CLI scripts (`generate_keypair.py`, `encrypt.py`, …) — one exercise each. They import
   `rsa_compute as compute` and `rsa_io as io`, and contain nothing but a `cli_args()` function and a
   `if __name__ == '__main__':` block that reads args, loads keys, calls compute, writes output.

**Conventions to preserve when writing new chapter code:**

- `cli_args(command=sys.argv[0], args=sys.argv[1:])` uses `match`/`case` over the argv tuple, with a
  `case _: raise SystemExit(f'Usage: {command} ...')` fallback. Defaults are bound at def time deliberately —
  it makes the function testable from the REPL.
- **All stdin/stdout code lives in `std_io.py`**, carried by every chapter: `read_text` / `write_text`,
  `read_binary` / `write_binary`, `write_pem`. `rsa_io` is key files only, `x509_io` certificate files only.
- Binary payloads (ciphertext, signatures) cross process boundaries **base64-armored** via
  `std_io.write_binary` / `std_io.read_binary`, so scripts pipe into each other.
- Prompts and output leads are printed **only when the stream is a TTY** — interactive use is friendly,
  piped use stays clean. This holds for *every* function in `std_io`; it is what makes the shell
  composition above work. A labelled field is just `write_text(value, lead='Subject: ')`.
- `_save_bytes` opens with `'xb'` and turns `FileExistsError` into a `SystemExit`: **key material is never
  silently overwritten.**
- Private-key passwords are optional; when absent, `get_private_bytes` prints an explicit
  `WARNING: Private key not encrypted!` to stderr rather than quietly doing the unsafe thing. Later chapters
  should keep making the insecure option visible instead of hiding it.
- Crypto choices already fixed: RSA 2048 / e=65537, OAEP with MGF1-SHA256 for encryption, PSS with
  `MAX_LENGTH` salt and SHA256 for signatures, PEM `TraditionalOpenSSL` for private keys,
  `SubjectPublicKeyInfo` for public keys, SHA256 for certificate and CSR signatures.
- `ca_io` defines its own `_save_bytes`, as `rsa_io` and `x509_io` already each do. Three near-identical
  private helpers is the accepted cost of keeping the `io` modules independent of one another.

## Generated files

`*.pem` is gitignored — key material, certificates, and CA files are produced by running the scripts and are
not committed. The two `alice-*.pem` files present in `01-rsa/` are local scratch output. Never commit PEMs,
and never rely on a specific one existing.
