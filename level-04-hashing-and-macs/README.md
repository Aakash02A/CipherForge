# 🏷️ Level 04: Cryptographic Hashing, MACs & AEAD

Welcome to **Level 04** of CipherForge. This level covers the trifecta of data integrity and authenticity: **Cryptographic Hash Functions**, **Message Authentication Codes (MAC)**, and **Authenticated Encryption with Associated Data (AEAD)**.

---

## 🎯 Educational Objectives

- Master the three pillars of cryptographic hash security:
  1. **Preimage Resistance (One-Way):** Given $h$, it is infeasible to find $m$ such that $H(m) = h$.
  2. **Second Preimage Resistance (Weak Collision):** Given $m_1$, it is infeasible to find $m_2 \neq m_1$ such that $H(m_1) = H(m_2)$.
  3. **Collision Resistance (Strong Collision):** It is infeasible to find any pair $m_1 \neq m_2$ such that $H(m_1) = H(m_2)$.
- Understand the **Birthday Paradox** and why an $n$-bit hash function offers only $n/2$ bits of collision security.
- Analyze **Length Extension Attacks** on Merkle-Damgård hashes and see how HMAC and SHA-3 sponge constructions mathematically prevent them.
- Learn why unauthenticated encryption fails and why **Authenticated Encryption with Associated Data (AEAD)** is the modern standard for all network and storage security.

---

## 🔬 Core Mathematical & Security Concepts

### 1. Merkle-Damgård vs. Sponge Construction
- **Merkle-Damgård (MD5, SHA-1, SHA-2):** Iteratively feeds fixed-size message blocks into a compression function $f$:
  $$s_i = f(s_{i-1}, m_i)$$
  Because the output hash is simply the final internal compression state $s_k$, an attacker who observes $H(m)$ can append extra padding and message data $m'$ to compute $H(m \parallel \text{pad} \parallel m')$ without knowing the original secret prefix. This is the **Length Extension Attack**!
- **Sponge Construction (SHA-3 / Keccak):** Operates on a state of $b = r + c$ bits, where $r$ is the *rate* and $c$ is the *capacity*. Message bits are absorbed into the rate part, followed by permutation rounds $f$, and squeezed out. The internal capacity $c$ is never exposed, rendering length extension attacks mathematically impossible.

### 2. Message Authentication Codes (MAC)
A hash function guarantees integrity against accidental corruption, but **not against an active adversary** who can recalculate the hash of modified data. A MAC requires a shared secret key $K$.

#### Why Not Simply $H(K \parallel M)$?
If $H$ is a Merkle-Damgård hash (e.g. SHA-256), an attacker observing $T = H(K \parallel M)$ can perform a length extension attack to forge a valid tag for $M \parallel \text{pad} \parallel \text{malicious}$ without ever knowing key $K$!

#### The HMAC Solution (RFC 2104)
HMAC sandwiches the inner hash inside an outer hash using two constant padding masks:
$$\text{HMAC}(K, M) = H\Big((K' \oplus \text{opad}) \;\parallel\; H\big((K' \oplus \text{ipad}) \;\parallel\; M\big)\Big)$$
- $\text{ipad} = \text{0x36}$ repeated to block size
- $\text{opad} = \text{0x5c}$ repeated to block size
This nested hashing effectively seals the internal state, provably stopping length extension attacks.

### 3. Authenticated Encryption with Associated Data (AEAD)
Encryption alone provides confidentiality, but **not authenticity**. An adversary intercepting ciphertext in CBC or CTR mode can flip bits or alter ciphertext blocks (Malleability / Bit-flipping attacks).

AEAD schemes (e.g., AES-GCM, ChaCha20-Poly1305) simultaneously provide:
1. **Confidentiality:** Plaintext is encrypted into ciphertext.
2. **Integrity & Authenticity:** A cryptographic authentication tag is produced over both the ciphertext and unencrypted Associated Data (AAD, such as packet headers, IP addresses, or sequence numbers).
3. **Tamper Detection:** Decryption fails immediately if even a single bit of ciphertext, AAD, or tag is modified.

```text
Plaintext ──► [Symmetric Cipher] ──► Ciphertext ──┬──► [Polynomial MAC] ──► Auth Tag
                     ▲                            │          ▲
                    Key                          AAD        Key
```

> [!CAUTION]
> ### The GCM Nonce-Reuse Disaster ("The Forbidden Attack")
> In Galois/Counter Mode (AES-GCM), authentication uses polynomial evaluation over the binary Galois field $GF(2^{128})$ via the hash key $H = E_K(0^{128})$.
> If the same `(Key, Nonce)` is reused across two different messages:
> 1. Keystream XOR reveals plaintext XOR: $C_1 \oplus C_2 = P_1 \oplus P_2$.
> 2. The difference of authentication tags yields a polynomial equation whose roots reveal the internal GHASH key $H$.
> Once $H$ is recovered, the adversary can forge arbitrary authentication tags for any message!

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm / Scheme | Real-World Context | Vulnerabilities & Attacks | Modern Recommendation |
| :--- | :--- | :--- | :--- |
| **MD5** | Legacy checksums, file verification | Practical collision attacks (Wang et al., 2004; Flame malware forged MD5 cert in 2012). | **Forbidden for security** |
| **SHA-1** | Git legacy commits, old SSL certificates | Full collision attack demonstrated (SHAttered, 2017). | **Deprecated** |
| **SHA-256 / SHA-512** | TLS, Bitcoin, DNSSEC, Linux shadow | Vulnerable to length extension if used as $H(K \parallel M)$; collision resistant. | **Approved Standard** |
| **SHA-3 (Keccak)** | Ethereum (Keccak-256), FIPS 202 standard | Sponge design immune to length extension; excellent resistance to side-channel analysis. | **Recommended** |
| **BLAKE3** | Fast file hashing, distributed filesystems | Tree-hashing mode allows parallel SIMD execution; out-performs SHA-256 by up to 10x. | **Top Performance Choice** |
| **HMAC-SHA256** | JWT authentication, API signatures, IPsec | None known; constant-time comparison (`secrets.compare_digest`) required to prevent timing leaks. | **Industry Standard** |
| **Poly1305** | WireGuard, TLS 1.3, Signal | One-time authenticator modulo $2^{130}-5$; catastrophic forgery if key/nonce is ever reused. | **Excellent with ChaCha20** |
| **AES-GCM** | TLS 1.3, IPsec, SSH, Google Tink | Catastrophic failure under nonce reuse; table-based $GF(2^{128})$ vulnerable to cache-timing without CLMUL. | **Standard (Ensure Unique Nonce)** |
| **ChaCha20-Poly1305** | TLS 1.3 on mobile, WireGuard | Constant-time software implementation; immune to cache-timing attacks on CPUs without AES-NI. | **Standard (Mobile & Embedded)** |

---

## 📂 Algorithm Index & Direct Modules

### 4.1 Cryptographic Hash Functions
| Algorithm | Digest Size | Architecture | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- | :--- |
| **MD5** | 128 bits | Merkle-Damgård (Broken) | [`hash-functions/MD5.py`](hash-functions/MD5.py) | `md5_menu` |
| **SHA-1** | 160 bits | Merkle-Damgård (Broken) | [`hash-functions/SHA_1.py`](hash-functions/SHA_1.py) | `sha1_menu` |
| **SHA-2** | 224/256/384/512 | Merkle-Damgård | [`hash-functions/SHA_2.py`](hash-functions/SHA_2.py) | `sha2_menu` |
| **SHA-3** | Variable (Keccak) | Sponge Construction | [`hash-functions/SHA_3.py`](hash-functions/SHA_3.py) | `sha3_menu` |
| **BLAKE2** | Up to 512 bits | HAIFA Construction | [`hash-functions/BLAKE2.py`](hash-functions/BLAKE2.py) | `blake2_menu` |
| **BLAKE3** | 256 bits | Tree Hashing & Bao | [`hash-functions/BLAKE3.py`](hash-functions/BLAKE3.py) | `blake3_menu` |
| **RIPEMD-160** | 160 bits | Dual-stream 160-bit | [`hash-functions/RIPEMD_160.py`](hash-functions/RIPEMD_160.py) | `ripemd160_menu` |
| **Whirlpool** | 512 bits | W block cipher (NESSIE) | [`hash-functions/Whirlpool.py`](hash-functions/Whirlpool.py) | `whirlpool_menu` |
| **Tiger** | 192 bits | 64-bit word design | [`hash-functions/Tiger.py`](hash-functions/Tiger.py) | `tiger_menu` |

### 4.2 Message Authentication Codes (MAC)
| Algorithm | Mechanism | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **HMAC** | Keyed nested hashing (RFC 2104) | [`message-authentication/HMAC.py`](message-authentication/HMAC.py) | `hmac_menu` |
| **CMAC** | Cipher-based MAC (NIST SP 800-38B) | [`message-authentication/CMAC.py`](message-authentication/CMAC.py) | `cmac_menu` |
| **GMAC** | Galois Field polynomial MAC | [`message-authentication/GMAC.py`](message-authentication/GMAC.py) | `gmac_menu` |
| **Poly1305** | High-speed prime field authenticator | [`message-authentication/Poly1305.py`](message-authentication/Poly1305.py) | `poly1305_menu` |

### 4.3 Authenticated Encryption (AEAD)
| Scheme | Cipher + Authenticator | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **AES-GCM** | AES-CTR + GHASH ($GF(2^{128})$) | [`authenticated-encryption/aesgcm.py`](authenticated-encryption/aesgcm.py) | `aesgcm_menu` |
| **AES-CCM** | AES-CTR + CBC-MAC | [`authenticated-encryption/aesccm.py`](authenticated-encryption/aesccm.py) | `aesccm_menu` |
| **ChaCha20-Poly1305** | ChaCha20 + Poly1305 (RFC 8439) | [`authenticated-encryption/chacha20poly1305.py`](authenticated-encryption/chacha20poly1305.py) | `chacha20poly1305_menu` |
| **AES-OCB** | Offset Codebook Single-pass AEAD | [`authenticated-encryption/ocb.py`](authenticated-encryption/ocb.py) | `ocb_menu` |

