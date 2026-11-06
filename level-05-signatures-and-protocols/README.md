# 📜 Level 05: Digital Signatures & Cryptographic Protocols

Welcome to **Level 05** of CipherForge. This level covers **Digital Signatures** (providing authenticity, data integrity, and non-repudiation) and **Secure Communication Protocols** (combining primitives into end-to-end secure network transport).

---

## 🎯 Educational Objectives

- Understand the three essential properties of digital signatures:
  1. **Authenticity:** Verifies the exact identity of the signer.
  2. **Integrity:** Proves the signed message was not altered in transit.
  3. **Non-repudiation:** The signer cannot dispute having signed the document.
- Contrast deterministic signatures with probabilistic signature schemes (e.g., RSA-PKCS1v1.5 vs. **RSA-PSS**).
- Analyze the catastrophic danger of **nonce reuse in DSA and ECDSA** (the famous Sony PlayStation 3 private key recovery).
- Explore **EdDSA (Ed25519)** and **Schnorr Signatures** (BIP-340) and see how deterministic nonces and linear properties enable signature aggregation.
- Dissect real-world cryptographic handshakes: **TLS 1.3**, **SSH-2**, **IPsec IKEv2**, **PGP Hybrid Encryption**, and **Kerberos**.

---

## 🔬 Core Mathematical & Security Concepts

### 1. Digital Signature Schemes
A signature scheme consists of three algorithms:
1. $\text{KeyGen}() \to (pk, sk)$
2. $\text{Sign}(sk, m) \to \sigma$
3. $\text{Verify}(pk, m, \sigma) \to \{\text{True}, \text{False}\}$

### 2. The ECDSA Nonce-Reuse Disaster (The PS3 Attack)
In ECDSA, signing message $m$ with private key $d$ requires choosing a random integer $k$ modulo curve order $n$:
$$R = k \cdot G = (x_1, y_1), \quad r = x_1 \pmod n$$
$$s \equiv k^{-1}(H(m) + d \cdot r) \pmod n$$

> [!CAUTION]
> ### What Happens If Nonce $k$ Is Reused?
> If a signer uses the same nonce $k$ to sign two distinct messages $m_1$ and $m_2$:
> $$s_1 - s_2 = k^{-1}\big(H(m_1) - H(m_2)\big) \pmod n$$
> Any observer can instantly calculate the secret nonce $k$:
> $$k = \frac{H(m_1) - H(m_2)}{s_1 - s_2} \pmod n$$
> And once $k$ is known, the private key $d$ is immediately recovered:
> $$d = \frac{s_1 \cdot k - H(m_1)}{r} \pmod n$$
> **In 2010, fail0verflow recovered Sony's master PS3 signing key because Sony's ECDSA code used a constant $k$ instead of a random number!**

### 3. EdDSA (Ed25519) — Deterministic Security
To eliminate random number generator failures completely, RFC 8032 (Ed25519) computes the nonce deterministically:
$$k = \text{SHA-512}(sk_{\text{hash\_prefix}} \parallel m)$$
Because $k$ is a cryptographic hash of the private key and the message, identical messages produce identical signatures, and different messages **never** share a nonce.

### 4. Schnorr Signatures & Linearity
Schnorr signatures replace ECDSA with a linear equation:
$$s = k + e \cdot d \pmod n, \quad \text{where } e = H(R \parallel pk \parallel m)$$
Because the signature equation is linear, multiple parties can combine their public keys and signatures:
$$\sum s_i = \sum k_i + e \cdot \sum d_i$$
This enables **Signature Aggregation** and **MuSig** in Bitcoin Taproot (BIP-340), dramatically reducing blockchain footprint.

### 5. Network Protocol Handshakes (TLS 1.3)
TLS 1.3 redesigned the internet's transport layer to complete handshakes in a single round trip (1-RTT):
```text
Client                                                   Server
ClientHello                                            
  + KeyShare (Client Ephemeral X25519) ────────►
                                                      ServerHello
                                                        + KeyShare (Server Ephemeral X25519)
                                                      {EncryptedExtensions}
                                                      {Certificate}
                                                      {CertificateVerify (Ed25519/RSA-PSS)}
                                       ◄────────────  {Finished}
[Handshake Complete — Both derive session keys via HKDF]
```

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm / Protocol | Real-World Context | Vulnerabilities & Attacks | Modern Recommendation |
| :--- | :--- | :--- | :--- |
| **RSA-PSS** | TLS 1.3, X.509 PKI certificates | Older PKCS#1 v1.5 susceptible to Bleichenbacher-style forgery; RSA-PSS provides provable security bounds. | **Recommended** (PSS with SHA-256) |
| **DSA** | Legacy FIPS 186-2/3 standard | Reused or predictable random $k$ leaks private key; fixed 1024-bit key size insecure. | **Deprecated** by NIST |
| **ECDSA** | Bitcoin (secp256k1), TLS 1.2 certificates | RNG failures / nonce bias leak private key; signature malleability ($s$ vs. $-s \pmod n$). | Use RFC 6979 deterministic $k$ |
| **Ed25519 (EdDSA)** | SSH keys, Signal, Tor onion v3, Solana | Highly optimized; immune to cache timing and nonce-leak bugs; fast verification. | **Top Modern Recommendation** |
| **Schnorr (BIP-340)** | Bitcoin Taproot, MuSig | Requires clean domain separation in hashing; simple algebraic verification. | **Standard for Multi-Signatures** |
| **TLS 1.3** | Web traffic (HTTPS), modern microservices | 0-RTT early data susceptible to replay attacks if not guarded by application layer. | **Internet Standard** |
| **SSH-2** | Remote server administration | Weak legacy key exchange algorithms (e.g. diffie-hellman-group1-sha1) disabled. | Use `curve25519-sha256` |
| **PGP / GPG** | Encrypted email, git commit verification | Symmetrically encrypts message with AES/CAST-128; encrypts session key with recipient RSA/ECC key. | Active for file/mail encryption |
| **Kerberos v5** | Windows Active Directory enterprise auth | Pass-the-Ticket, Golden Ticket, and Kerberoasting attacks if weak DES/RC4 ciphers are enabled. | Secure with AES-256-CTS-HMAC |

---

## 📂 Algorithm Index & Direct Modules

### 5.1 Digital Signatures
| Algorithm | Key Standard | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **RSA Signatures** | PKCS#1 v1.5 & PSS | [`digital-signatures/RSA_Signature.py`](digital-signatures/RSA_Signature.py) | `rsa_signature_menu` |
| **DSA** | FIPS 186-4 Discrete Log | [`digital-signatures/dsa.py`](digital-signatures/dsa.py) | `dsa_menu` |
| **ECDSA** | SECP256k1 / NIST Curves | [`digital-signatures/ECDSA.py`](digital-signatures/ECDSA.py) | `ecdsa_menu` |
| **EdDSA** | Edwards-curve RFC 8032 | [`digital-signatures/EdDSA.py`](digital-signatures/EdDSA.py) | `eddsa_menu` |
| **Schnorr** | Linear Signature (BIP-340) | [`digital-signatures/Schnorr.py`](digital-signatures/Schnorr.py) | `schnorr_menu` |

### 5.2 Cryptographic Protocols
| Protocol | Scope | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **TLS 1.3** | Transport Layer Security Simulation | [`protocols/tls.py`](protocols/tls.py) | `tls_menu` |
| **IPsec IKEv2** | Internet Protocol Security Key Exchange | [`protocols/ipsec.py`](protocols/ipsec.py) | `ipsec_menu` |
| **SSH-2** | Secure Shell Transport & Key Exchange | [`protocols/ssh.py`](protocols/ssh.py) | `ssh_menu` |
| **PGP / OpenPGP** | Asymmetric + Symmetric Hybrid Envelope | [`protocols/pgp.py`](protocols/pgp.py) | `pgp_menu` |
| **Kerberos** | KDC Ticket Granting Service (TGS) | [`protocols/kerberos.py`](protocols/kerberos.py) | `kerberos_menu` |

