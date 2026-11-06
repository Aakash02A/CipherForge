# 📈 CipherForge Interactive Learner Progress Tracker

Welcome to your personal mastery roadmap through **CipherForge**! Use this document to track your progress as you work through all 8 levels of cryptographic algorithms, attack simulations, and the capstone project.

---

## 🏆 Learner Milestone Badges

Track your journey through the levels. As you complete each level, mark the checklist below and celebrate your progress!

| Level | Milestone Badge | Focus Area | Status |
| :---: | :---: | :--- | :---: |
| **01** | ![Level 01](https://img.shields.io/badge/Level_01-Classical_Ciphers-0288d1?style=for-the-badge&logo=python&logoColor=white) | Substitution, Transposition & Rotors | [ ] Complete |
| **02** | ![Level 02](https://img.shields.io/badge/Level_02-Symmetric_Crypto-512da8?style=for-the-badge&logo=python&logoColor=white) | SPN, Feistel, Cipher Modes & Streams | [ ] Complete |
| **03** | ![Level 03](https://img.shields.io/badge/Level_03-Asymmetric_&_DH-388e3c?style=for-the-badge&logo=python&logoColor=white) | RSA, Discrete Logs, ECC & X25519 | [ ] Complete |
| **04** | ![Level 04](https://img.shields.io/badge/Level_04-Hashing_&_AEAD-f57c00?style=for-the-badge&logo=python&logoColor=white) | SHA-2/3, BLAKE3, HMAC, GCM & Poly1305 | [ ] Complete |
| **05** | ![Level 05](https://img.shields.io/badge/Level_05-Signatures_&_Protocols-c2185b?style=for-the-badge&logo=python&logoColor=white) | Ed25519, Schnorr, TLS 1.3 & SSH | [ ] Complete |
| **06** | ![Level 06](https://img.shields.io/badge/Level_06-Password_&_KDF-00796b?style=for-the-badge&logo=python&logoColor=white) | PBKDF2, BCrypt, Scrypt, Argon2id & HKDF | [ ] Complete |
| **07** | ![Level 07](https://img.shields.io/badge/Level_07-Advanced_&_PQC-7b1fa2?style=for-the-badge&logo=python&logoColor=white) | ML-KEM (Kyber), ML-DSA, FHE, ZKP & SSSS | [ ] Complete |
| **08** | ![Level 08](https://img.shields.io/badge/Level_08-Capstone_SecureVault-fbc02d?style=for-the-badge&logo=python&logoColor=black) | End-to-End Encrypted Vault & Messaging CLI | [ ] Complete |

---

## 📜 Level 01: Classical & Historical Ciphers
- [ ] Understand monoalphabetic vs. polyalphabetic substitution.
- [ ] Perform frequency analysis on a Caesar ciphertext.
- [ ] Understand Kasiski examination and index of coincidence for the Vigenère cipher.
- [ ] Compute modular inverses for the Hill cipher 2×2 matrix.
- [ ] Explore the Enigma machine simulator and verify that no letter encrypts to itself.
- [ ] Test the Rail Fence transposition cipher with varying rail depths.

---

## 🔐 Level 02: Symmetric Key Cryptography
- [ ] Compare Feistel networks (DES, Blowfish) vs. Substitution-Permutation Networks (AES).
- [ ] Understand Shannon's Confusion and Diffusion.
- [ ] Explore why ECB mode leaks plaintext patterns (the ECB Penguin effect).
- [ ] Understand CBC mode initialization vectors and padding oracle vulnerabilities.
- [ ] Test Counter (CTR) mode and understand keystream generation.
- [ ] Explore Galois/Counter Mode (GCM) authenticated encryption.
- [ ] Trace stream ciphers (ChaCha20, Salsa20) and observe keystream reuse cancellation:
  $$C_1 \oplus C_2 = P_1 \oplus P_2$$

---

## 🔑 Level 03: Asymmetric / Public Key & Key Exchange
- [ ] Explain the Integer Factorization Problem (IFP) and RSA key generation:
  $$e \cdot d \equiv 1 \pmod{\phi(N)}$$
- [ ] Understand why textbook RSA without padding (OAEP) is insecure.
- [ ] Simulate the Diffie-Hellman key agreement protocol.
- [ ] Understand the Elliptic Curve Discrete Logarithm Problem (ECDLP).
- [ ] Compare NIST Weierstrass curves with modern Montgomery (Curve25519) and Edwards curves (Ed25519).
- [ ] Understand Paillier additive homomorphic encryption.

---

## 🏷️ Level 04: Cryptographic Hashing, MACs & AEAD
- [ ] Define the 3 hash security properties: Preimage, Second Preimage, and Collision Resistance.
- [ ] Explain why the Birthday Paradox reduces $n$-bit security to $n/2$ bits.
- [ ] Contrast Merkle-Damgård iterative hashing with the Keccak (SHA-3) sponge construction.
- [ ] Demonstrate why $H(K \parallel M)$ is vulnerable to length extension attacks.
- [ ] Study the nested structure of HMAC-SHA256.
- [ ] Understand polynomial MACs (GMAC and Poly1305).
- [ ] Test AEAD schemes (AES-GCM and ChaCha20-Poly1305) and observe automatic tag validation.

---

## ✍️ Level 05: Digital Signatures & Protocols
- [ ] Explain the three guarantees of digital signatures: Authenticity, Integrity, Non-repudiation.
- [ ] Understand the fatal vulnerability of nonce reuse in ECDSA (Sony PS3 key leak).
- [ ] Study deterministic nonce generation in Ed25519 (RFC 8032).
- [ ] Explore linear properties and key aggregation in Schnorr signatures (BIP-340).
- [ ] Trace the 1-RTT handshake of TLS 1.3 (ClientHello $\to$ ServerHello $\to$ HKDF).
- [ ] Understand PGP/OpenPGP hybrid encryption (asymmetric envelope wrapping symmetric session key).

---

## 🛡️ Level 06: Password Hashing & Key Derivation (KDF)
- [ ] Understand why fast hashes (SHA-256) must never be used for user passwords.
- [ ] Benchmark PBKDF2 iteration counts and verify NIST/OWASP recommendations ($\ge 600,000$ rounds).
- [ ] Explore BCrypt cost factor ($2^{\text{cost}}$ rounds) and salt formatting.
- [ ] Understand Scrypt memory-hardness and parameter tuning ($N, r, p$) against ASIC rigs.
- [ ] Master Argon2id (RFC 9106) time, memory, and thread parameters.
- [ ] Learn HKDF Extract-then-Expand key derivation (RFC 5869) for protocol key schedules.

---

## ⚛️ Level 07: Modern, Advanced & Post-Quantum Cryptography
- [ ] Understand why Shor's Algorithm breaks RSA, DH, and ECC on a quantum computer.
- [ ] Study the NIST Post-Quantum Standards:
  - [ ] CRYSTALS-Kyber (ML-KEM / FIPS 203)
  - [ ] CRYSTALS-Dilithium (ML-DSA / FIPS 204)
  - [ ] SPHINCS+ (SLH-DSA / FIPS 205)
- [ ] Test Shamir's $(k, n)$ Threshold Secret Sharing Scheme using Lagrange interpolation.
- [ ] Study Fully Homomorphic Encryption (FHE) arithmetic over encrypted ciphertexts.
- [ ] Explore Yao's Garbled Circuits and 1-out-of-2 Oblivious Transfer (OT).
- [ ] Learn the fundamentals of Zero-Knowledge Proofs: Completeness, Soundness, and Zero-Knowledge (Schnorr ZKP, zk-SNARKs).

---

## 🏆 Level 08: Capstone Project (SecureVault CLI)
- [ ] Run the SecureVault interactive application: `python -m level-08-capstone-project.secure_vault`.
- [ ] Encrypt a document into a `.vault` container with PBKDF2 key derivation and AES-256-GCM.
- [ ] Verify file decryption and SHA-256 integrity match.
- [ ] Execute an End-to-End Encrypted Messaging (E2EE) exchange between Alice and Bob using ephemeral X25519 and Ed25519 signatures.
- [ ] Run the active bit-flip tamper simulation and verify that AEAD prevents unauthorized modification.

