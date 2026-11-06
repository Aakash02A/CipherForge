# 🔑 Level 03: Asymmetric Key Cryptography & Key Exchange

Welcome to **Level 03** of CipherForge. Asymmetric cryptography (public-key cryptography) solves the fundamental problem of symmetric encryption: **how do two parties agree on a secret key over an insecure channel without meeting in person?**

---

## 🎯 Educational Objectives

- Understand the mathematical foundation of **trapdoor one-way functions**: easy to compute in one direction, computationally infeasible to invert without secret trapdoor information.
- Study the three core hardness assumptions of modern public-key crypto:
  1. **Integer Factorization Problem (IFP):** RSA, Rabin.
  2. **Discrete Logarithm Problem (DLP):** Diffie-Hellman, ElGamal, MQV.
  3. **Elliptic Curve Discrete Logarithm Problem (ECDLP):** ECDH, X25519, Ed25519.
- Learn why **textbook public-key encryption is catastrophically insecure** and why randomized padding schemes (like RSA-OAEP) are mandatory.
- Explore elliptic curve group operations: point addition, point doubling, scalar multiplication ($k \cdot P$), and Montgomery laddering.

---

## 🔬 Core Mathematical & Security Concepts

### 1. The Integer Factorization Problem (RSA)
RSA relies on the difficulty of finding the prime factors $p$ and $q$ of a large composite modulus $N = p \cdot q$:
$$\phi(N) = (p - 1)(q - 1)$$
$$e \cdot d \equiv 1 \pmod{\phi(N)}$$
Encryption: $c \equiv m^e \pmod N$. Decryption: $m \equiv c^d \pmod N$.

> [!WARNING]
> **Textbook RSA Danger:** If $c = m^e \pmod N$ without padding:
> 1. Deterministic encryption: An adversary can encrypt dictionary guesses to identify $m$.
> 2. Homomorphic malleability: $E(m_1) \cdot E(m_2) = (m_1 \cdot m_2)^e \pmod N = E(m_1 \cdot m_2)$.
> Modern implementations MUST use **RSA-OAEP** (Optimal Asymmetric Encryption Padding) to achieve IND-CCA2 security.

### 2. Diffie-Hellman Key Agreement (DLP)
Alice and Bob agree on public group parameters $(p, g)$ where $p$ is a large safe prime and $g$ is a generator.
```text
Alice (Private: a)                              Bob (Private: b)
Public: A = g^a mod p                          Public: B = g^b mod p
         │                                              │
         ├────────────── Public A ─────────────────────►│
         │◄───────────── Public B ──────────────────────┤
         │                                              │
Computes: K = B^a mod p                        Computes: K = A^b mod p
            = (g^b)^a mod p                               = (g^a)^b mod p
            = g^(ab) mod p                                = g^(ab) mod p
```
An eavesdropper seeing $g, p, A, B$ cannot efficiently compute $g^{ab} \pmod p$ without solving the **Computational Diffie-Hellman (CDH)** problem.

### 3. Elliptic Curve Cryptography (ECDLP)
An elliptic curve over a finite field $\mathbb{F}_p$ follows the Weierstrass equation:
$$y^2 \equiv x^3 + ax + b \pmod p$$
Points on the curve form an abelian group under a chord-and-tangent geometric addition law.
- **Scalar Multiplication:** Given base generator point $G$ and private scalar $d$, computing $Q = d \cdot G$ is fast via double-and-add ($O(\log d)$).
- **Hardness:** Finding $d$ given $Q$ and $G$ requires $O(\sqrt{p})$ operations (Pollard's rho), requiring far smaller keys than RSA (256-bit ECC matches the security of 3072-bit RSA!).

### 4. Modern Twisted Edwards & Montgomery Curves (Curve25519 / X25519)
Daniel J. Bernstein designed Curve25519 ($y^2 = x^3 + 486662x^2 + x$ over $2^{255} - 19$) to achieve:
- **Immunity to timing attacks:** Constant-time Montgomery ladder using only the $x$-coordinate.
- **No invalid-curve attacks:** Every 32-byte sequence is a valid curve point or quadratic twist point.

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm / Scheme | Real-World Context | Vulnerabilities & Attacks | Modern Status |
| :--- | :--- | :--- | :--- |
| **RSA (OAEP)** | TLS 1.2 certificates, PGP, code signing | Bleichenbacher's chosen-ciphertext attack on PKCS#1 v1.5 padding; timing attacks on modular exponentiation. | Secure with $\ge 2048$-bit keys and OAEP/PSS |
| **Diffie-Hellman (Finite Field)** | SSH, IPsec, legacy TLS | Logjam attack on 512/768-bit export groups; small-subgroup confinement attacks if peer keys are not validated. | Use safe primes ($\ge 2048$-bit) or migrate to ECDH |
| **ECDH (Weierstrass curves)** | TLS 1.2/1.3 (NIST P-256, P-384) | Side-channel timing in scalar multiplication; invalid curve attacks if points are not checked on-curve. | Good with vetted libraries |
| **X25519** | TLS 1.3, Signal Protocol, WireGuard | None known; constant-time by design; simple Montgomery ladder math eliminates point-validation bugs. | **Gold Standard** for modern key exchange |
| **ElGamal** | GnuPG, cryptographic voting | 2x ciphertext expansion; completely broken if ephemeral random $k$ is reused across messages. | Historical / Academic |
| **Paillier** | Privacy-preserving voting, federated ML | Slower than standard RSA; ciphertexts grow to $N^2$; malleable by design (additive homomorphism). | Specialized privacy applications |
| **Rabin Cryptosystem** | Provable security benchmark | Decryption yields 4 possible roots (requires disambiguation); vulnerable to chosen-ciphertext attack. | Academic foundation |

---

## 📂 Algorithm Index & Direct Modules

### 3.1 Public Key Encryption
| Algorithm | Underlying Hardness | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **RSA** | Integer Factorization Problem | [`public-key-encryption/rsa.py`](public-key-encryption/rsa.py) | `rsa_menu` |
| **ElGamal** | Discrete Logarithm Problem | [`public-key-encryption/ElGamal.py`](public-key-encryption/ElGamal.py) | `elgamal_menu` |
| **Rabin** | Modular Square Roots (Equivalent to IFP) | [`public-key-encryption/Rabin.py`](public-key-encryption/Rabin.py) | `rabin_menu` |
| **Paillier** | Decisional Composite Residuosity | [`public-key-encryption/Paillier.py`](public-key-encryption/Paillier.py) | `paillier_menu` |

### 3.2 Key Exchange & Agreement
| Protocol | Type | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **Diffie-Hellman** | Finite Field Key Agreement | [`key-exchange/DiffieHellman.py`](key-exchange/DiffieHellman.py) | `dh_menu` |
| **ECDH** | Elliptic Curve Key Agreement | [`key-exchange/ECDH.py`](key-exchange/ECDH.py) | `ecdh_menu` |
| **X25519** | Montgomery Ladder Curve25519 | [`key-exchange/X25519.py`](key-exchange/X25519.py) | `x25519_menu` |
| **MQV** | Authenticated Diffie-Hellman | [`key-exchange/MQV.py`](key-exchange/MQV.py) | `mqv_menu` |

### 3.3 Elliptic Curve Primitives
| Module | Curve Standard | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **Ed25519** | Edwards-curve Twisted Model | [`elliptic-curves/Ed25519.py`](elliptic-curves/Ed25519.py) | `ed25519_menu` |
| **ECC ECDH** | Weierstrass Point Operations | [`elliptic-curves/ECDH.py`](elliptic-curves/ECDH.py) | `ecdh_menu` |
| **ECC ECDSA** | Point Scalar Multiplication | [`elliptic-curves/ECDSA.py`](elliptic-curves/ECDSA.py) | `ecdsa_menu` |

