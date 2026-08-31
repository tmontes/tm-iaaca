# Timing

Measured estimates for the material as actually built, against the schedule in `outline.md`.
That schedule is the original design; this file is what the chapters turned out to cost.

**Method.** Script counts are exact. Minutes assume ~8 min for the first script in a chapter
(learning the conventions), ~4 min for later ones, ~2–3 min for a reciprocal variant, ~1 min per
command run, 1–2 min per discussion question. Workshop pace is set by the slowest third of the
room, not the median, so treat these as optimistic.

**Already applied:** `generate_keypair.py` is given in every chapter rather than written, and
`04-tls`'s `bob.local` break-it bullet is gone (it duplicated `06-broken` drill 2). Both are folded
into the numbers below.


## Where the time goes

| Chapter | `outline.md` | Scripts to write | Commands | Estimate | Driver |
|---|---:|---:|---:|---:|---|
| 0 — setup and story | 10 | — | — | 10 | fine as budgeted |
| `01-rsa` | 20 | 4 | ~8 | **22** | 4 scripts, plus first contact with `lib/`, `cli_args`, piping |
| `01-rsa` §4 *(optional)* | — | 2 | ~6 | **+14** | not in the original budget |
| `02-certificates` | 20 | 3 | ~9 | **24** | `inspect_certificate.py` is the longest script; REPL expiry |
| `03-ca` | 20 | 2 | ~14 | **25** | `issue_certificate.py` has the 4-argument CLI; two CAs to set up |
| `04-tls` | 15 | 2 | ~14 | **22** | first multi-terminal work; 4 server launches; 5 fetches |
| `05-mitm` | 25 | 0 | ~18 | **32** | 3 terminals, 5 process starts/stops, reading hex |
| `06-broken` | 10 | 0 (+1 optional edit) | ~13 | **18** | 4 certificates × issue, launch, fetch |
| **Total** | **120** | **11** | | **~153** | |

**As built, this is a 2h30–2h45 workshop.** About 28% over the two-hour slot, assuming no
environment problems and a room that keeps pace.

The original estimate drifted in two ways: Part 1 was always tight, and Parts 4–6 each grew —
chapter 4 gained the plain-HTTP opening and a second issuing script, chapter 5 gained the whole
wiretap section, chapter 6 gained the CN-only drill and the optional inspection upgrade.


## Shape A — three hours, unchanged

Everything stays participant-written, `01-rsa` §4 becomes a genuinely reachable optional section,
and there is slack for stragglers. This is what the material currently is.


## Shape B — two hours, by giving more scripts away

Participants still type 11 scripts; that remains the dominant cost. Converting more of them to
worked examples costs about a third of the time and *lowers* risk.

| Change | Saves |
|---|---:|
| Give `decrypt.py` and `verify.py`; write `encrypt.py` and `sign.py` | 6 min |
| `05-mitm` §1 wiretap as an instructor demo; participants do only the MITM scenarios | 8 min |
| `06-broken`: two of the four drills hands-on, the other two as discussion | 8 min |
| Drop `01-rsa` §4 entirely | 14 min |

Lands near 117 minutes with every chapter still hands-on, at the cost of `01-rsa` thinning to two
written scripts.


## Release valves

Places to skip when running late, in the order I would spend them:

1. `06-broken` §1 (optional inspection upgrade) — already marked optional.
2. `02-certificates` §3, the expired-certificate REPL bullet — chapter 6 covers expiry.
3. `03-ca` §3, the second break-it bullet.
4. `05-mitm` §1 HTTP half — but the HTTP/TLS contrast *is* the section, so cutting half guts it.


## Independent of length

Make `uv sync` and a Python 3.12 check **pre-work**, sent out before the session. It is not in the
153 minutes, and a room discovering toolchain problems at minute 5 loses 10–15 minutes of the
budget there is least of.


## Undecided

Which shape. Depends on the slot length, which may not be ours to choose. Both are costed above;
the schedule table in `outline.md` still reflects the original two-hour design and will need
rewriting once the shape is settled.
