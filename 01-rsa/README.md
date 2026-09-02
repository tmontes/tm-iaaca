# RSA Fundamentals

You are given:

* A library of modules, under `lib/`, containing `rsa_compute.py` and `rsa_io.py`
  for RSA key handling and operations, and `std_io.py` to read and write the terminal;
  import them with `from lib import rsa_compute` and create your scripts next to `lib/`.

* The `create_keypair.py` script that generates RSA key pairs;
  it is the shape all of these scripts take - read it before writing your own.

* A reciprocal `decrypt.py` and `verify.py`, so you can exercise the `encrypt.py` and `sign.py`
  you write below without also having to write their other half.

In this context *plain text* is human-readable text (`str` objects)
while *ciphertext* is a binary payload (`bytes` objects);
the functions in `std_io.py` may come in handy to read/write these things.


## 1. Generate an RSA Key Pair

* Read `create_keypair.py`: a `cli_args()` that matches on the command line,
  then a `__main__` block that reads arguments, calls `compute`, and writes with `io`.
  Nothing else. Yours could look like this - or quite different, of course.

* Use it to generate key pairs for **Alice** and **Bob**.

* Look at the two files it wrote for each of them:
  they are ASCII text files in the so-called PEM format.
  Which one could you publish, and what happens to the other if you lose it?


## 2. Encrypt and Decrypt

* Create an `encrypt.py` script that
  encrypts a given plain text message with a given public key.

* You are given a reciprocal `decrypt.py`, which
  decrypts a ciphertext payload with a given private key.

* Exercise your script, and the given one, by having:
  * **Alice** encrypt a message to **Bob**, confirming **Bob** successfully decrypts it.
  * **Bob** respond with an encrypted message to **Alice**, confirming she decrypts it too.

* Try encrypting a message longer than 190 bytes.
  RSA encrypts small payloads only - real systems use it to wrap a symmetric key instead.


## 3. Sign and Verify

* Create a `sign.py` script that
  generates a signature from a given plain text message and private key.

* You are given a `verify.py`, which
  verifies a plain text message signature with a given public key.

* Exercise your script, and the given one, by having a message signed by **Alice** and then:
  * Verify it was signed by **Alice**.
  * Verify it was not signed by **Bob**.


## 4. Parting Thoughts

**Alice** and **Bob** can now exchange messages no one else can read,
and prove to each other who wrote them.

Those guarantees rest on two files named `alice-public.pem` and `bob-public.pem`.
Who told **Bob** that key is **Alice**'s and vice-versa?

RSA binds a signature to a *key*.
Binding a key to an *identity* is what certificates are for.
