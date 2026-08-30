# Trust Me, I'm a Certificate Authority

*A hands-on introduction to RSA, X.509, PKI, TLS, and MITM attacks with Python*

## Tutorial format

**Duration:** 2 hours  
**Style:** Interactive / live coding  
**Audience:** Python developers with basic Python knowledge  
**Approach:** Instructor presents a concept and a small piece of code; participants implement and explore it themselves.

### Tools

- Python
- `cryptography`
- `flask`
- `hypercorn`
- `requests`
- Web browser — optional

### Core narrative

> **Alice wants to talk securely to Bob. Eve wants to listen. Who should Alice trust?**

Participants progressively build the answer by implementing the cryptographic pieces themselves.

---

# Schedule

| Time | Chapter | Main concept |
|---:|---|---|
| 0–10 min | 🎭 The setup | Alice, Bob, and Eve |
| 10–30 min | 🔑 RSA fundamentals | Keys, encryption, signatures |
| 30–50 min | 📜 Certificates | X.509, Subject, Issuer, identity |
| 50–70 min | 🏛️ Become a CA | Certificate signing and trust chains |
| 70–85 min | 🤝 Real HTTPS | Client/server trust with Flask + Requests |
| 85–110 min | 😈 MITM | Interception and trust anchors |
| 110–120 min | 🧩 Break the PKI | Diagnose deliberately broken certificates |

---

# 0–10 min — 🎭 The Setup

Start with a problem rather than a PKI lecture.

Alice wants to communicate securely with Bob.

```text
Alice                         Bob
  │                             │
  │─────── HTTPS? ─────────────>│
  │                             │
```

Ask the audience:

> Alice wants to know two things:
>
> 1. Nobody can read what she sends Bob.
> 2. She is actually talking to Bob.

Introduce Eve:

```text
Alice                  Eve                  Bob
  │                     │                    │
  ├────────────────────>│───────────────────>│
  │                     │                    │
```

Ask:

> **How can Alice know she's really talking to Bob?**

Don't answer yet.

This question drives the rest of the tutorial.

---

# 10–30 min — 🔑 Part 1: RSA Fundamentals

## Exercise 1 — Generate an RSA key pair

Participants generate an RSA private key and derive its public key.

```python
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()
```

Discuss:

- Private vs public key
- Why the private key must remain secret
- Why the public key can be distributed

Core observation:

> **The private key is secret. The public key isn't.**

---

## Exercise 2 — Encrypt and decrypt

Alice encrypts using Bob's public key.

```text
Alice
  │
  │ "hello Bob"
  ▼
Bob's public key
  │
  ▼
ciphertext
  │
  ▼
Bob's private key
  │
  ▼
"hello Bob"
```

Participants implement RSA encryption/decryption using OAEP.

Key takeaway:

```text
public key  → encrypt
private key → decrypt
```

---

## Exercise 3 — Sign and verify

Now reverse the conceptual direction.

Bob signs a message using his private key.

Alice verifies the signature using Bob's public key.

```text
private key → sign
public key  → verify
```

Ask:

> **What does this allow Alice to establish?**

Then ask the crucial follow-up:

> **But how did Alice get Bob's public key?**

Transition:

> We need a way to bind a public key to an identity.

---

# 30–50 min — 📜 Part 2: Certificates

Introduce X.509 certificates.

Conceptually:

```text
Certificate
┌───────────────────────────┐
│ Subject: Bob              │
│ Public key: ...           │
│ Issuer: ???               │
│ Valid from: ...           │
│ Valid until: ...          │
│ Serial: ...               │
│ Signature: ...             │
└───────────────────────────┘
```

## Exercise 4 — Create a certificate

Participants use `cryptography.x509` to create a certificate.

Have them inspect:

```python
cert.subject
cert.issuer
cert.serial_number
cert.not_valid_after_utc
cert.public_key()
```

Introduce:

- Subject
- Issuer
- Public key
- Validity period
- Serial number
- Certificate signature

Initially create a self-signed certificate:

```text
Issuer  = Bob
Subject = Bob
```

Ask:

> **Bob issued a certificate saying Bob is Bob. Why should Alice believe it?**

This introduces the need for a Certificate Authority.

---

# 50–70 min — 🏛️ Part 3: Become a Certificate Authority

Participants become their own CA.

Create:

```text
                    Workshop Root CA
                           │
                           │ signs
                           ▼
                         Bob
```

Generate:

```text
ca-private-key.pem
ca-certificate.pem

bob-private-key.pem
bob-certificate.pem
```

Bob's certificate now contains:

```text
Subject = Bob
Issuer  = Workshop Root CA
```

## Exercise 5 — Issue a certificate

Participants:

1. Generate the CA key.
2. Create the CA certificate.
3. Generate Bob's key.
4. Create Bob's certificate.
5. Sign Bob's certificate with the CA key.
6. Inspect the resulting certificate.

Core concept:

> **A CA vouches for the binding between an identity and a public key.**

Trust chain:

```text
Bob's certificate
       │
       │ signed by
       ▼
Workshop Root CA
       │
       │ trusted by Alice
       ▼
     Alice
```

---

## Exercise 6 — Which certificate should Alice trust?

Give participants two certificates:

```text
bob-cert.pem
eve-cert.pem
```

Both should look legitimate.

Ask:

> **Which one should Alice trust?**

The answer:

> Not because the certificate "looks right", but because of its issuer and whether that issuer is trusted.

---

# 70–85 min — 🤝 Part 4: Make It Real

Now use Flask + Hypercorn to create an actual HTTPS service.

Participants run something like:

```text
https://localhost:8443
```

with their generated certificate.

The browser can optionally be used here, but the canonical client should be Python.

## Exercise 7 — Connect with Requests

Initially:

```python
requests.get("https://localhost:8443")
```

Expected result:

```text
❌ CERTIFICATE_VERIFY_FAILED
```

Ask:

> The connection is encrypted. Why does it fail?

Answer:

> **Encryption and trust are different things.**

Now explicitly configure the CA:

```python
requests.get(
    "https://localhost:8443",
    verify="ca-certificate.pem",
)
```

Result:

```text
✅ 200 OK
```

Conceptual chain:

```text
Certificate
     │
     ▼
Issuer
     │
     ▼
CA
     │
     ▼
Trust configuration
     │
     ▼
TLS connection accepted
```

Key takeaway:

> **HTTPS being encrypted does not automatically mean the peer is trusted.**

---

# 85–110 min — 😈 Part 5: The MITM

Return to the opening diagram.

```text
Alice              Eve               Bob
  │                 │                 │
  │── HTTPS ───────>│── HTTPS ───────>│
  │                 │                 │
  │<────────────────│<────────────────│
```

Eve wants to impersonate Bob.

## Exercise 8 — Create Eve's certificate

Eve creates:

```text
eve-private-key
eve-certificate
```

Eve presents the certificate as if she were Bob.

Initially:

```text
Alice
  │
  │ HTTPS
  ▼
Eve
  │
  │ "I am Bob!"
  ▼
Alice

❌ Certificate rejected
```

Ask:

> **Why doesn't this work?**

Because Eve's certificate isn't trusted.

---

## Exercise 9 — The trust-anchor attack

Use an isolated test trust configuration.

Give the client the ability to trust Eve's CA:

```python
requests.get(
    "https://bob.local",
    verify="evil-ca.pem",
)
```

Now:

```text
Alice
  │
  │ trusts Evil CA
  ▼
Eve
  │
  ▼
Bob
```

Result:

```text
😱 MITM SUCCESS
```

Ask:

> **What changed?**

Not:

- RSA
- encryption
- HTTPS
- the certificate format

The crucial change was:

> **The trust anchor.**

Core lesson:

> **PKI security ultimately depends on which certificate authorities the client trusts.**

---

# 110–120 min — 🧩 Part 6: Break the PKI

Finish with a rapid-fire debugging exercise.

Give participants deliberately broken certificates.

## Broken certificate 1 — Wrong issuer

```text
Subject: bob.local
Issuer: Evil CA
```

Client trusts:

```text
Workshop CA
```

Question:

> Why is this rejected?

---

## Broken certificate 2 — Wrong hostname

Certificate:

```text
SAN = alice.local
```

Request:

```text
https://bob.local
```

Question:

> The certificate is signed by a trusted CA. Why does it still fail?

Introduce hostname verification and Subject Alternative Names.

---

## Broken certificate 3 — Expired

```text
Not After: yesterday
```

Question:

> What part of the certificate's validity is being checked?

---

## Broken certificate 4 — Wrong CA

Client trusts:

```text
Workshop CA
```

Certificate signed by:

```text
Totally Legit CA™
```

Question:

> Is a valid certificate necessarily a trusted certificate?

Answer:

> **No.**

---

# Final Recap

Return to the original question:

> **How can Alice know she's really talking to Bob?**

Build the final model:

```text
                         TRUST
                           │
                           ▼
                    ┌─────────────┐
                    │   Root CA   │
                    └──────┬──────┘
                           │
                         signs
                           │
                           ▼
                  Bob's certificate
                           │
                    contains public key
                           │
                           ▼
Alice ─────────────── TLS ────────────── Bob
  │                                      ▲
  │                                      │
  └────────────── Eve ───────────────────┘
                       │
                       └── ❌ untrusted
```

The participants have now built the complete chain:

```text
RSA keys
   ↓
signatures
   ↓
X.509 certificates
   ↓
Certificate Authorities
   ↓
trust chains
   ↓
TLS
   ↓
MITM protection
```

## The final message

> **PKI isn't magic.**
>
> It's a system for answering one deceptively difficult question:
>
> **“Why should I believe that this public key belongs to who it claims to belong to?”**
>
> And the answer is:
>
> **“Because someone I already trust said so.”**

---

# Things deliberately out of scope

Don't try to cover everything PKI-related in two hours.

Skip:

- CRLs
- OCSP
- ACME / Let's Encrypt
- Production CA architecture
- Complex intermediate CA hierarchies
- Certificate transparency
- TLS cipher suites
- TLS handshake internals
- Elliptic-curve cryptography
- Browser/OS global trust stores
- PEM vs DER details

If asked about these, acknowledge them and move on:

> “Excellent question. That's how we turn this two-hour tutorial into a two-day workshop.”

---

# Workshop philosophy

The tutorial should feel less like:

> “Here's how PKI works.”

and more like:

> “Here's a problem. Let's write some Python and find out.”

Each section should follow the same rhythm:

1. **Present a problem**
2. **Explain just enough theory**
3. **Show a tiny piece of code**
4. **Participants implement it**
5. **Break it**
6. **Investigate why it broke**
7. **Use the result to motivate the next concept**

The audience should leave having **constructed and broken a miniature PKI**, rather than having listened to a lecture about one.