# 🛣️ CipherForge Curated Learning Tracks

Not everyone has time to explore all 90+ algorithms at once. Depending on your current objectives—whether preparing for security engineering interviews, building real-world enterprise PKI systems, or researching post-quantum cryptography—use these curated learning paths.

---

## 🎯 Track 1: 2-Week Security Engineering Interview Sprint
*Target: Software Engineers, DevOps/SREs, and Security Engineers preparing for systems and security architecture interviews.*

### Week 1: Foundations, Symmetric Crypto & Authenticity
- **Day 1:** [Level 02: Block Ciphers & Modes](level-02-symmetric-crypto/README.md)
  - Study AES structure (SPN), difference between 128/256-bit keys.
  - Deep dive: Why ECB mode leaks structure; why CBC mode requires random IVs.
- **Day 2:** [Level 02: Stream Ciphers & Nonce Discipline](level-02-symmetric-crypto/stream-ciphers/README.md)
  - Understand keystream XOR; what happens when nonces are reused ($C_1 \oplus C_2 = P_1 \oplus P_2$).
  - ChaCha20 vs. AES-NI hardware trade-offs.
- **Day 3:** [Level 04: Hashing & Length Extension](level-04-hashing-and-macs/README.md)
  - Preimage vs. Collision resistance.
  - Why $H(K \parallel M)$ is broken on SHA-256; how HMAC solves it.
- **Day 4:** [Level 04: Authenticated Encryption (AEAD)](level-04-hashing-and-macs/authenticated-encryption/README.md)
  - AES-GCM and ChaCha20-Poly1305. The catastrophic consequence of GCM nonce reuse.
- **Day 5:** [Level 06: Password Hashing Best Practices](level-06-password-and-kdf/README.md)
  - Salting, peppering, and why SHA-256 is unacceptable for credentials.
  - Compare PBKDF2 vs. BCrypt vs. Scrypt vs. Argon2id.

### Week 2: Asymmetric Crypto, PKI & Capstone
- **Day 6:** [Level 03: Public-Key Cryptography](level-03-asymmetric-crypto/README.md)
  - RSA mathematical basics; why textbook RSA ($c = m^e \pmod N$) is broken without OAEP.
  - Diffie-Hellman discrete logarithm key agreement.
- **Day 7:** [Level 03: Elliptic Curves & X25519](level-03-asymmetric-crypto/elliptic-curves/README.md)
  - Weierstrass curves vs. Montgomery curves (Curve25519).
  - Why 256-bit ECC matches 3072-bit RSA security.
- **Day 8:** [Level 05: Digital Signatures](level-05-signatures-and-protocols/README.md)
  - ECDSA vs. Ed25519 (EdDSA).
  - The fatal ECDSA reused nonce attack (Sony PS3 key leak).
- **Day 9:** [Level 05: TLS 1.3 Handshake](level-05-signatures-and-protocols/protocols/README.md)
  - 1-RTT flow, ephemeral Diffie-Hellman for Forward Secrecy, key schedule via HKDF.
- **Day 10:** [Level 08: Capstone Review](level-08-capstone-project/README.md)
  - Inspect the E2EE messaging and File Vault architecture in [`level-08-capstone-project/secure_vault.py`](level-08-capstone-project/secure_vault.py).

---

## 📜 Track 2: Classical to Modern Crypto Track
*Target: Computer Science students, educators, and cryptography enthusiasts seeking a chronological and mathematical journey.*

- **Phase 1: Pen, Paper & Rotors (Level 01)**
  - Caesar cipher shift math over $\mathbb{Z}_{26}$.
  - Vigenère polyalphabetic cipher & Kasiski attack.
  - Hill cipher matrix inversions modulo 26.
  - WWII Enigma rotor stepping and reciprocal reflector flaw.
- **Phase 2: The Digital Revolution & Shannon's Principles (Level 02)**
  - Shannon's Confusion and Diffusion.
  - Feistel networks: DES (56-bit key) and 3DES.
  - The AES competition: Rijndael, Twofish, Serpent.
- **Phase 3: Asymmetric Revolution (Level 03 & Level 05)**
  - Merkle, Diffie, and Hellman's 1976 breakthrough.
  - Rivest, Shamir, and Adleman (RSA) 1977 factorization.
  - Digital signatures and public key infrastructure (PKI).
- **Phase 4: Modern Standards & The Quantum Horizon (Level 06 & Level 07)**
  - Argon2id password hashing.
  - Post-quantum lattice schemes (Kyber, Dilithium).

---

## 🛡️ Track 3: Applied Cybersecurity Specialist
*Target: Penetration testers, AppSec engineers, and enterprise security architects.*

- **Core Security Pitfalls to Master:**
  1. **ECB Mode Leakage:** Visualizing plaintext repetition in encrypted data.
  2. **Padding Oracle Attacks:** Breaking CBC mode when decryption errors leak timing/responses.
  3. **Hash Length Extension:** Forging API requests using naïve SHA-256 signatures.
  4. **ECDSA Nonce Biasing:** Recovering private keys from biased random number generators.
  5. **Sweet32 Attack:** Explaining 64-bit block collisions on 3DES and Blowfish.
  6. **Bit-Flipping Attacks:** Modifying unauthenticated CBC/CTR ciphertexts and preventing it via AEAD.
- **Hands-On Exercises:**
  - Run the Capstone tamper simulation in [`level-08-capstone-project/secure_vault.py`](level-08-capstone-project/secure_vault.py) to test tag failure on altered payloads.

---

## ⚛️ Track 4: Privacy-Preserving & Post-Quantum Frontier
*Target: Cryptographic researchers, Web3/blockchain developers, and data privacy specialists.*

- **Module 1: Post-Quantum Cryptography (PQC)**
  - Shor's algorithm and the vulnerability of RSA/ECC.
  - NIST FIPS 203: CRYSTALS-Kyber (ML-KEM) lattice key encapsulation.
  - NIST FIPS 204: CRYSTALS-Dilithium (ML-DSA) lattice signatures.
  - NIST FIPS 205: SPHINCS+ (SLH-DSA) stateless hash signatures.
- **Module 2: Privacy-Preserving Computation**
  - Paillier Partially Homomorphic Encryption (PHE): additive computation on encrypted ballots.
  - Fully Homomorphic Encryption (FHE): BFV/CKKS concepts for cloud inference.
  - Shamir's $(k, n)$ Threshold Secret Sharing: key recovery without single points of failure.
  - Secure Multi-Party Computation: Oblivious Transfer and Yao's Garbled Circuits.
- **Module 3: Zero-Knowledge Proofs (ZKP)**
  - Interactive Schnorr zero-knowledge protocol.
  - zk-SNARKs: Succinct non-interactive proofs (Groth16) and arithmetic circuits.
  - zk-STARKs: Transparent post-quantum scalable arguments.

