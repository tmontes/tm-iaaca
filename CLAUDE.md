# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Teaching material for a 2-hour interactive PyCon PT 2026 tutorial: *Trust Me, I'm a Certificate Authority* —
participants build a miniature PKI (RSA → X.509 → CA → TLS → MITM) themselves, in Python.

**`outline.md` is the authoritative spec** for content, sequencing, timing, and — importantly — what is
*deliberately out of scope* (CRLs, OCSP, ACME, intermediate CA hierarchies, TLS handshake internals, ECC,
PEM vs DER details). Read it before adding material; don't broaden scope beyond it.

The narrative thread is Alice / Bob / Eve and the single question "how can Alice know she's really talking to Bob?".
Code should serve that narrative — small, readable, composable at the shell, and breakable on purpose.

## Layout and status

Chapter directories map 1:1 onto `outline.md` parts:

| Dir | Outline part | Status |
|---|---|---|
| `01-rsa/` | Part 1 — RSA fundamentals | implemented |
| `02-certificates/` | Part 2 — X.509 certificates | empty |
| `03-ca/` | Part 3 — become a CA | empty |
| `04-tls/` | Part 4 — Flask/Waitress HTTPS + Requests | empty |
| `05-mitm/` | Part 5–6 — MITM and broken certificates | empty |

Each chapter has its own `README.md` — the participant-facing exercise brief (numbered exercises, describing
which scripts *they* write and which support modules are given to them). The root `README.md` is still empty.

## Commands

`uv`-managed project, `requires-python >= 3.14`. Dependencies: `cryptography`, `flask`, `waitress`, `requests`.

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
who fell behind start any chapter clean. The cost is duplication: **a fix to a carried-over module must be
propagated to every chapter that carries it**, and the copies are expected to stay byte-identical
(`diff` them). Participants carry their own `*.pem` files and their own scripts forward by hand.

The reference scripts at each chapter root (`encrypt.py`, `create_certificate.py`, …) are **solutions, not
handouts** — participants write their own. Producing the participant copy of a chapter means removing the
root-level `*.py` and keeping `README.md` + `lib/`.

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
  `SubjectPublicKeyInfo` for public keys.

## Generated files

`*.pem` is gitignored — key material, certificates, and CA files are produced by running the scripts and are
not committed. The two `alice-*.pem` files present in `01-rsa/` are local scratch output. Never commit PEMs,
and never rely on a specific one existing.
