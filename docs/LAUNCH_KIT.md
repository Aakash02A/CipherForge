# 🚀 CipherForge Social Media Launch Kit

Ready-to-use, high-engagement promotional templates formatted specifically for LinkedIn, Reddit, and X (Twitter) to share **CipherForge** with the developer and cybersecurity communities.

---

## 🤖 Reddit Post Template: r/crypto & r/cryptography

**Title:** `CipherForge: An open-source educational repository covering 90+ cryptographic algorithms across 8 progressive levels (Classical -> Post-Quantum -> E2EE Capstone)`

```markdown
Hey everyone!

Over the past few months, we've been building **CipherForge**—an educational, community-driven repository designed to help students, developers, and security enthusiasts explore cryptographic algorithms from first principles with runnable Python code and transparent step-by-step breakdowns.

GitHub: https://github.com/Aakash02A/CipherForge

### 🗺️ Curriculum Structure (8 Levels):
1. **Level 01: Classical & Historical Ciphers** — Caesar, Vigenère (with Kasiski attack demo), Playfair, Hill (matrix inversions mod 26), WWII Enigma simulator, and Rail Fence.
2. **Level 02: Symmetric Key Cryptography** — SPN vs. Feistel networks; AES, DES, 3DES, Blowfish, Twofish, Camellia, Serpent; 8 block cipher modes (with visual demonstrations of why ECB mode leaks patterns); stream ciphers (ChaCha20, Salsa20, RC4) and why nonce reuse destroys keystreams ($C_1 \oplus C_2 = P_1 \oplus P_2$).
3. **Level 03: Asymmetric Cryptography & Key Exchange** — RSA with OAEP padding, ElGamal, Rabin, Paillier (additive homomorphism), Diffie-Hellman, ECDH, and X25519 Montgomery ladders.
4. **Level 04: Cryptographic Hashing, MACs & AEAD** — Merkle-Damgård vs. Sponge (SHA-3); length extension attack mechanics; HMAC-SHA256, CMAC, Poly1305; AES-GCM and the catastrophic danger of GCM nonce reuse.
5. **Level 05: Digital Signatures & Protocols** — RSA-PSS, DSA, ECDSA (demonstrating the PlayStation 3 nonce-reuse key recovery attack), Ed25519 deterministic signing, Schnorr linear signatures (BIP-340); simulations of TLS 1.3 1-RTT, SSH-2, and IPsec IKEv2.
6. **Level 06: Password Hashing & Key Derivation (KDF)** — Why fast hashes fail; benchmarking PBKDF2 iterations; BCrypt work factors; Scrypt memory hardness against ASICs; Argon2id (RFC 9106); and HKDF Extract-then-Expand (RFC 5869).
7. **Level 07: Modern, Advanced & Post-Quantum Cryptography** — Lattice-based ML-KEM (Kyber) and ML-DSA (Dilithium); hash-based SPHINCS+; Shamir's (k, n) Secret Sharing; Fully Homomorphic Encryption (FHE); Yao's Garbled Circuits / Oblivious Transfer; and interactive Schnorr ZKPs / zk-SNARKs.
8. **Level 08: Capstone Project (SecureVault CLI)** — A complete, runnable End-to-End Encrypted File Vault and Secure Messaging CLI combining X25519 ECDH, Ed25519 signatures, HKDF, and AES-GCM / ChaCha20-Poly1305 with automatic bit-flip tamper detection.

We've also built an interactive terminal UI (`python main.py`), automated CI tests, and curated learning tracks (e.g. 2-Week Security Interview Sprint).

We'd love feedback on the pedagogical explanations, docstrings, or suggestions for additional attack simulations. Contributions are very welcome!
```

---

## 🎓 Reddit Post Template: r/learnprogramming

**Title:** `I created an open-source cryptography learning toolkit: 90+ algorithms explained step-by-step from Classical Ciphers to Post-Quantum Crypto (Python)`

```markdown
Hi all!

A lot of computer science students and self-taught developers find cryptography intimidating because tutorials either stay too high-level ("just call `encrypt()`") or drown in abstract abstract algebra without showing real code.

To fix that, I transformed **CipherForge** into an open-source, hands-on cryptography learning repository:
👉 https://github.com/Aakash02A/CipherForge

### What makes it special for learners:
- **8 Progressive Levels:** Starts with simple pen-and-paper ciphers (Caesar, Vigenère) where you can easily follow the math, and gradually builds up to modern symmetric ciphers, public-key crypto, digital signatures, password hashing, and post-quantum lattice cryptography.
- **Learn By Breaking Things:** We explicitly demonstrate *broken* algorithms alongside modern ones. You can see the classic "ECB penguin" pattern leakage, simulate how reusing a nonce in a stream cipher decrypts secret messages, and run a tamper attack simulation where flipping a single bit in an encrypted vault is detected and blocked by AEAD.
- **Interactive Terminal Menu:** Just clone the repo and run `python main.py` to step through interactive menus for all algorithms.
- **Capstone Project:** Level 08 includes a full End-to-End Encrypted File Vault and Secure Messaging tool showing how all these pieces fit together in real-world software.

Hope this helps anyone studying cybersecurity, prepping for interviews, or curious about how encryption actually works!
```

---

## 🐦 X / Twitter Thread Template

```text
🧵 1/6: Most engineers use encryption daily, but how many know what actually happens when bytes are encrypted?

Introducing CipherForge: An open-source, community-driven educational toolkit covering 90+ cryptographic algorithms across 8 progressive levels! 🔐

⭐ https://github.com/Aakash02A/CipherForge

---

2/6: Rather than treating cryptography as a black-box API, CipherForge teaches through inner mechanics and attack simulations:
• Why does ECB mode leak images?
• Why does nonce reuse in ECDSA leak the private key?
• Why is SHA-256 catastrophic for storing passwords?

---

3/6: Organized into 8 progressive levels:
📜 Level 01: Classical & Historical Ciphers
🔐 Level 02: Symmetric Key Cryptography & Modes
🔑 Level 03: Asymmetric / Public Key & Diffie-Hellman
🏷️ Level 04: Cryptographic Hashing, MACs & AEAD

---

4/6:
✍️ Level 05: Digital Signatures & Network Protocols (TLS 1.3)
🛡️ Level 06: Password Hashing & KDFs (Argon2id, BCrypt, Scrypt)
⚛️ Level 07: Modern, Advanced & Post-Quantum (Kyber, Dilithium, ZKP, FHE)
🏆 Level 08: SecureVault Capstone CLI

---

5/6: Includes:
✅ Interactive CLI (`python main.py`)
✅ Built-in diagnostics checking all 90 modules
✅ Curated learning tracks (Interview sprint, AppSec track)
✅ Capstone with active bit-flip tamper attack simulation

---

6/6: Check out the repo, star if you find it helpful, and feel free to contribute test vectors, attack scripts, or new algorithms! 🚀

https://github.com/Aakash02A/CipherForge
```
