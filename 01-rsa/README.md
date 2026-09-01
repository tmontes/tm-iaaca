# RSA Fundamentals

The `lib/` directory holds the modules you are given: `rsa_compute.py` and `rsa_io.py`
for keys, `std_io.py` to read and write the terminal. Import them as
`from lib import rsa_compute as compute`, and write your own scripts next to `lib/`.

`generate_keypair.py` is given too, and every chapter has a copy.
It is the shape all of these scripts take — read it before writing your own.

In this context *plain text* is human-readable text (Python `str` objects)
while *ciphertext* is a binary payload (Python `bytes` objects);
the functions in `std_io.py` may come in handy to read/write these things.


## 1. Generate an RSA Key Pair

* Read `generate_keypair.py`: a `cli_args()` that matches on the command line,
  then a `__main__` block that reads arguments, calls `compute`, and writes with `io`.
  Nothing else. Yours will look like this.

* Use it to generate key pairs for **Alice** and **Bob**.

* Look at the two files it wrote for each of them.
  Which one could you publish, and what happens to the other if you lose it?


## 2. Encrypt and Decrypt


* Create an `encrypt.py` script:
  encrypts a given plain text message with a given public key.

* Create a reciprocal `decrypt.py` script:
  decrypts a ciphertext payload with a given private key.

* Exercise your scripts by having:
  *  **Alice** encrypt a message to **Bob**, confirming **Bob** successfully decrypts it.
  *  **Bob** responding with an encrypted message to **Alice**, that can also decrypt it.

* Try encrypting a message longer than 190 bytes.
  RSA encrypts small payloads only — real systems use it to wrap a symmetric key instead.


## 3. Sign and Verify

* Create a `sign.py` script:
  generates a signature from a given plain text message and private key.

* Create a `verify.py` script:
  verifies a plain text message signature with a given public key.

* Exercise your scripts by having a message signed by **Alice** and then:
  * Verify it was signed by **Alice**.
  * Verify it was not signed by **Bob**.


## 4. Private and Authenticated Messaging (optional)

Combine the two:
a message only the recipient can read,
that only the sender could have written.

* Create a `send.py` script: signs and encrypts a given plain text message.

* Create a reciprocal `receive.py` script: decrypts and verifies.

* Exercise them by having **Alice** and **Bob** exchange private, authenticated messages.

Then break it:

* Tamper with the ciphertext.

* Keep the ciphertext, but swap in a signature from a different message.
  Which of the two guarantees survives?

* Generate a key pair for **Eve** and have her send **Bob** a message,
  which he receives using **Alice**'s public key.
  He decrypts it perfectly — what does verification tell him that decryption cannot?


## 5. Parting Thoughts

**Alice** and **Bob** can now exchange messages no one else can read,
and prove to each other who wrote them.

Those guarantees rest on two files named `alice-public.pem` and `bob-public.pem`.
Who told **Bob** that key is **Alice**'s and vice-versa?

RSA binds a signature to a *key*.
Binding a key to an *identity* is what certificates are for.
