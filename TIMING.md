# Timing

Measured estimates for the material as actually built. The "budget" column is the original
two-hour design; this file is what the chapters turned out to cost.

**Method.** Script counts are exact. Minutes assume ~8 min for the first script in a chapter
(learning the conventions), ~4 min for later ones, ~2–3 min for a reciprocal variant, ~1 min per
command run, 1–2 min per discussion question. Workshop pace is set by the slowest third of the
room, not the median, so treat these as optimistic.

**Already applied:** `generate_keypair.py` is given in every chapter rather than written; the
`bob.local` break-it bullet is gone from the TLS material (it duplicated `05-broken` drill 2); and
the CA and TLS chapters have been merged. All three are folded into the numbers below.


## Where the time goes

| Chapter | Budget | Scripts to write | Commands | Estimate | Driver |
|---|---:|---:|---:|---:|---|
| 0 — setup and story | 10 | — | — | 10 | fine as budgeted |
| `01-rsa` | 20 | 4 | ~8 | **22** | 4 scripts, plus first contact with `lib/`, `cli_args`, piping |
| `01-rsa` §4 *(optional)* | — | 2 | ~6 | **+14** | not in the original budget |
| `02-certificates` | 20 | 3 | ~9 | **24** | `inspect_certificate.py` is the longest script; REPL expiry |
| `03-ca-tls` | 35 | 3 | ~24 | **36** | 4 server launches; 5 fetches; two CAs; `issue_certificate.py` has the 4-argument CLI |
| `04-mitm` | 25 | 0 | ~18 | **32** | 3 terminals, 5 process starts/stops, reading hex |
| `05-broken` | 10 | 0 (+1 optional edit) | ~13 | **18** | 4 certificates × issue, launch, fetch |
| **Total** | **120** | **10** | | **~142** | |

**As built, this is a 2h20–2h35 workshop.** About 18% over the two-hour slot, assuming no
environment problems and a room that keeps pace.

### What the merge bought

Merging the CA and TLS chapters took the pair from 47 minutes to 36, and one written script off the
total:

* The CA setup was done twice — once per chapter, in two self-contained directories. Now once. (~3 min)
* `issue_server_certificate.py` is gone. Host names arrive in the CSR, so the same
  `issue_certificate.py` issues both certificates. (~4 min)
* The trust comparison was done twice: by hand in the CA chapter, then again by the TLS client. The
  hand inspection survives; the manual signature check is now a parenthetical, since the client does
  it on every connection. (~4 min)

Against that, the CSR costs ~2 minutes to read and run — both `create_csr.py` and
`create_server_csr.py` are given, not written.

The remaining overrun is Part 1 (always tight), `04-mitm`'s wiretap section, and `05-broken`'s CN-only
drill and optional inspection upgrade.


## Shape A — two and a half hours, unchanged

Everything stays participant-written, `01-rsa` §4 becomes a genuinely reachable optional section,
and there is slack for stragglers. This is what the material currently is.


## Shape B — two hours, by giving more scripts away

Participants still type 10 scripts; that remains the dominant cost. Converting more of them to
worked examples costs about a fifth of the time and *lowers* risk.

| Change | Saves |
|---|---:|
| Give `decrypt.py` and `verify.py`; write `encrypt.py` and `sign.py` | 6 min |
| `04-mitm` §1 wiretap as an instructor demo; participants do only the MITM scenarios | 8 min |
| `05-broken`: two of the four drills hands-on, the other two as discussion | 8 min |
| Drop `01-rsa` §4 entirely | 14 min |

Lands near 120 minutes with `01-rsa` §4 dropped and any two of the others, with every chapter still
hands-on.


## Release valves

Places to skip when running late, in the order I would spend them:

1. `05-broken` §1 (optional inspection upgrade) — already marked optional.
2. `02-certificates` §3, the expired-certificate REPL bullet — `05-broken` covers expiry.
3. `03-ca-tls` §5, the closing break-it bullet.
4. `04-mitm` §1 HTTP half — but the HTTP/TLS contrast *is* the section, so cutting half guts it.


## Independent of length

Make `uv sync` and a Python 3.12 check **pre-work**, sent out before the session. It is not in the
142 minutes, and a room discovering toolchain problems at minute 5 loses 10–15 minutes of the
budget there is least of.


## Undecided

Which shape. Depends on the slot length, which may not be ours to choose. Both are costed above.
