# ⚛️ Level 07: Modern, Advanced & Post-Quantum Cryptography

Welcome to **Level 07** of CipherForge. This level enters the cutting-edge frontier of theoretical and applied cryptography: **Post-Quantum Cryptography (PQC)** resistant to quantum computers, **Homomorphic Encryption**, **Secret Sharing**, **Secure Multi-Party Computation (MPC)**, and **Zero-Knowledge Proofs (ZKP)**.

---

## 🎯 Educational Objectives

- Understand the catastrophic threat of quantum computing to classical public-key cryptography:
  - **Shor's Algorithm (1994):** Solves Integer Factorization (RSA) and Discrete Logarithms (DH, ECDH, ECDSA) in polynomial time $O((\log N)^3)$.
  - **Grover's Algorithm (1996):** Speeds up unstructured brute force from $O(N)$ to $O(\sqrt{N})$, effectively halving the security level of symmetric ciphers (e.g. AES-128 drops to 64-bit security; AES-256 remains secure with 128-bit quantum security).
- Explore the mathematical foundations of the new NIST Post-Quantum Standards:
  - **Lattice-based cryptography:** Module Learning with Errors (M-LWE) and Short Integer Solution (SIS).
  - **Code-based cryptography:** Goppa error-correcting codes (Classic McEliece).
  - **Hash-based signatures:** Merkle tree and Winternitz one-time signature combinations (SPHINCS+).
- Study **Privacy-Preserving Computation**: computing over encrypted data (FHE) without decrypting it.
- Master **Zero-Knowledge Proofs**: proving possession of a secret without revealing a single bit of information about it.

---

## 🔬 Core Mathematical & Security Concepts

### 1. Lattice-Based Cryptography (ML-KEM / Kyber & ML-DSA / Dilithium)
Lattices are discrete periodic grids of points in $n$-dimensional Euclidean space. The security of lattice schemes relies on the hardness of:
- **Shortest Vector Problem (SVP):** Finding the non-zero lattice vector with minimum Euclidean norm.
- **Learning With Errors (LWE):** Given linear equations with small Gaussian noise $e$:
  $$\mathbf{b} \equiv \mathbf{A} \cdot \mathbf{s} + \mathbf{e} \pmod q$$
  Distinguishing $\mathbf{b}$ from a uniformly random vector is computationally intractable even for quantum computers.

### 2. Post-Quantum NIST Standards Overview
```text
           ┌───────────────────────────────────────────────┐
           │      NIST Post-Quantum Cryptography           │
           └───────────────────────┬───────────────────────┘
                                   │
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
   Key Encapsulation (KEM)                      Digital Signatures
   • ML-KEM (CRYSTALS-Kyber) [Lattice]          • ML-DSA (CRYSTALS-Dilithium) [Lattice]
   • NTRU [Lattice]                             • FN-DSA (Falcon) [Lattice]
   • Classic McEliece [Code-based]              • SLH-DSA (SPHINCS+) [Hash-based]
```

### 3. Shamir's $(k, n)$ Threshold Secret Sharing Scheme (SSSS)
To divide a master secret $S$ among $n$ participants such that any $k$ participants can reconstruct it, but any $k-1$ participants learn **zero information**:
1. Construct a random polynomial of degree $k-1$ in a finite field $\mathbb{F}_p$:
   $$f(x) = S + a_1 x + a_2 x^2 + \dots + a_{k-1} x^{k-1} \pmod p$$
2. Distribute share $(i, f(i))$ to participant $i$ for $i \in \{1, \dots, n\}$.
3. Reconstruct $S = f(0)$ using **Lagrange Polynomial Interpolation**:
   $$f(0) = \sum_{j=1}^k y_j \prod_{\substack{1 \le m \le k \\ m \neq j}} \frac{-x_m}{x_j - x_m} \pmod p$$

### 4. Fully Homomorphic Encryption (FHE)
Traditional encryption requires decrypting ciphertext to perform computations, exposing data in memory. Homomorphic encryption allows operations on ciphertexts directly:
$$\text{Dec}(c_1 \oplus c_2) = m_1 + m_2 \pmod N \quad (\text{Additive: Paillier})$$
$$\text{Dec}(c_1 \otimes c_2) = m_1 \times m_2 \quad (\text{Fully Homomorphic: BFV / CKKS})$$
Enables secure outsourced cloud analytics, private AI inference, and encrypted medical records queries.

### 5. Zero-Knowledge Proofs (ZKP)
A prover Peggy convinces verifier Victor that a statement is true without revealing why:
1. **Completeness:** If the statement is true, an honest verifier will be convinced.
2. **Soundness:** If the statement is false, no cheating prover can convince the verifier (except with negligible probability).
3. **Zero-Knowledge:** The verifier learns nothing beyond the fact that the statement is true.
- **zk-SNARKs:** Succinct, Non-interactive Arguments of Knowledge (requires trusted setup or transparent CRS; widely used in Zcash, Ethereum rollups).
- **zk-STARKs:** Scalable, Transparent ARguments of Knowledge (transparent, post-quantum secure, using collision-resistant hash functions instead of elliptic curve pairings).

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm / Domain | Real-World Context | Key Characteristics & Trade-offs | Modern Recommendation |
| :--- | :--- | :--- | :--- |
| **CRYSTALS-Kyber (ML-KEM)** | TLS 1.3 hybrid post-quantum (X25519Kyber768 in Chrome/Cloudflare) | Fast key generation and encapsulation; small public keys (~1184 bytes). | **NIST Standard (FIPS 203)** |
| **CRYSTALS-Dilithium (ML-DSA)** | Post-quantum code signing, PKI | Uniform lattice signature security; balanced signature and public key sizes. | **NIST Standard (FIPS 204)** |
| **Falcon (FN-DSA)** | Constrained network environments | Extremely compact signatures (~666 bytes), but requires floating-point math vulnerable to timing leaks. | **NIST Standard** |
| **SPHINCS+ (SLH-DSA)** | Conservative long-term archiving | Relies only on collision-resistant hash security (zero lattice hardness risk), but signatures are large (~8–40 KB). | **NIST Standard (FIPS 205)** |
| **Classic McEliece** | High-security post-quantum vaulting | Decades of cryptanalysis since 1978; huge public keys (~1 MB) limit network use. | **Top Confidence for Storage** |
| **Paillier Cryptosystem** | Electronic voting tallying, private telemetry | Efficient additive operations; does not support arbitrary multiplication without interactive protocols. | **Widely Used in Privacy** |
| **Shamir's Secret Sharing** | Cryptocurrency multi-sig, HSM disaster recovery | Information-theoretically secure; shares must be transmitted over authentic secure channels. | **Industry Standard for Keys** |
| **zk-SNARKs (Groth16)** | Blockchain privacy (Zcash), Layer-2 rollups | Constant-size proof (128 bytes) and verification in milliseconds; requires a trusted setup ceremony. | **Production Standard** |

---

## 📂 Algorithm Index & Direct Modules

### 7.1 Post-Quantum Key Encapsulation (KEMs)
| Algorithm | Family | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **CRYSTALS-Kyber** | Module-LWE Lattice (FIPS 203) | [`post-quantum-kems/kyber.py`](post-quantum-kems/kyber.py) | `kyber_menu` |
| **NTRU** | Ring-Lattice Polynomial | [`post-quantum-kems/ntru.py`](post-quantum-kems/ntru.py) | `ntru_menu` |
| **Classic McEliece** | Goppa Code-Based | [`post-quantum-kems/mceliece.py`](post-quantum-kems/mceliece.py) | `mceliece_menu` |

### 7.2 Post-Quantum Digital Signatures
| Algorithm | Family | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **CRYSTALS-Dilithium** | Module-SIS Lattice (FIPS 204) | [`post-quantum-signatures/dilithium.py`](post-quantum-signatures/dilithium.py) | `dilithium_menu` |
| **Falcon** | NTRU-Lattice Fast-Fourier | [`post-quantum-signatures/falcon.py`](post-quantum-signatures/falcon.py) | `falcon_menu` |
| **SPHINCS+** | Stateless Hash-Based (FIPS 205) | [`post-quantum-signatures/sphincsplus.py`](post-quantum-signatures/sphincsplus.py) | `sphincsplus_menu` |

### 7.3 Advanced & Privacy-Preserving Cryptography
| Algorithm | Paradigm | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **FHE** | Fully Homomorphic Encryption | [`homomorphic-encryption/fhe.py`](homomorphic-encryption/fhe.py) | `fhe_menu` |
| **PHE** | Partially Homomorphic (Paillier) | [`homomorphic-encryption/phe.py`](homomorphic-encryption/phe.py) | `phe_menu` |
| **Shamir Secret Sharing** | Polynomial Threshold Sharing | [`secret-sharing/Shamir_s_Secret_Sharing.py`](secret-sharing/Shamir_s_Secret_Sharing.py) | `shamir_menu` |
| **SMPC** | Secure Multi-Party Computation | [`secure-computation/smpc.py`](secure-computation/smpc.py) | `smpc_menu` |
| **Oblivious Transfer** | 1-out-of-2 OT Primitive | [`secure-computation/ot.py`](secure-computation/ot.py) | `ot_menu` |
| **Interactive ZKP** | Schnorr Zero-Knowledge Proof | [`zero-knowledge-proofs/zkp.py`](zero-knowledge-proofs/zkp.py) | `zkp_menu` |
| **zk-SNARKs** | Succinct Non-Interactive Arguments | [`zero-knowledge-proofs/zksnark.py`](zero-knowledge-proofs/zksnark.py) | `zksnark_menu` |
| **zk-STARKs** | Scalable Transparent Arguments | [`zero-knowledge-proofs/zkstark.py`](zero-knowledge-proofs/zkstark.py) | `zkstark_menu` |

