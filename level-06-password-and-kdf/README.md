# 🛡️ Level 06: Password Hashing & Key Derivation (KDF)

Welcome to **Level 06** of CipherForge. This level addresses one of the most critical topics in practical software engineering: **how to securely store user credentials and derive cryptographic keys from human passphrases.**

---

## 🎯 Educational Objectives

- Understand the fundamental difference between **Data Hashing** (optimized for speed and low CPU overhead) and **Password Hashing** (intentionally designed to be computationally slow and resource-intensive).
- Analyze the threat of **GPU, FPGA, and custom ASIC password-cracking rigs** capable of testing hundreds of billions of SHA-256 hashes per second.
- Study the progression of password hashing standards:
  1. **PBKDF2:** Iterative stretching (CPU-hard).
  2. **BCrypt:** Adaptive cost based on Blowfish key scheduling.
  3. **Scrypt:** Memory-hard key derivation to defeat ASICs.
  4. **Argon2:** State-of-the-art hybrid memory/time function (Password Hashing Competition winner).
- Master **HKDF (HMAC-based Extract-and-Expand KDF)** used to derive multiple cryptographically independent keys from a shared secret.

---

## 🔬 Core Mathematical & Security Concepts

### 1. The Password Hashing Dilemma: Why Fast Hashes Fail
A fast hash function like SHA-256 is designed to process gigabytes of data quickly:
- A modern GPU cluster can compute **over 100,000,000,000 SHA-256 hashes per second**.
- If a database leak contains passwords hashed with plain SHA-256, an 8-character password will be cracked in less than 2 minutes via dictionary or mask attacks!

Password hashing functions must therefore enforce **tunable computational work** and **memory consumption**:

```text
User Password ──► [Salt Generator] ──► [Memory-Hard / Iterative KDF] ──► Storage Hash
                       ▲                             ▲
                 16+ Random Bytes           NIST / OWASP Cost Settings
```

### 2. Salting vs. Peppering
- **Salt (Random Nonce):** A unique, cryptographically random value (minimum 16 bytes) generated per user and stored in plaintext alongside the hash.
  - **Purpose:** Defeats precomputed rainbow tables and ensures that two users with identical passwords have completely different hashes.
- **Pepper (Secret Key):** A high-entropy secret stored outside the database (e.g. in a Hardware Security Module or KMS).
  - **Purpose:** Protects hashes even if the database is dumped by an SQL injection attack.

### 3. Memory-Hardness (Scrypt & Argon2)
CPU-bound functions like PBKDF2 require almost no RAM to execute. A hardware designer can fit thousands of parallel hashing cores onto a tiny silicon wafer (an ASIC or FPGA).

**Memory-hard functions** force each computation to allocate and randomly access large blocks of RAM (e.g., 64 MB per hash). Because memory chips are physically large and expensive to replicate thousands of times on silicon, ASICs lose their cost-performance advantage against ordinary consumer CPUs.

### 4. HKDF: Extract-then-Expand (RFC 5869)
When two parties perform Diffie-Hellman key agreement, the resulting shared secret is mathematically uniform over the curve, but not necessarily a cryptographically uniform pseudorandom bit string.

HKDF safely transforms this into multiple independent keys:
1. **HKDF-Extract(salt, IKM) $\to$ PRK:** Concentrates entropy using HMAC.
2. **HKDF-Expand(PRK, info, L) $\to$ OKM:** Expands into cryptographically independent sub-keys using a domain-separation label (`info`).

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm | Real-World Context | Vulnerabilities & Attacks | Modern Recommendation |
| :--- | :--- | :--- | :--- |
| **PBKDF2** | WPA2-PSK, iOS keychain, legacy web frameworks | Zero memory hardness; vulnerable to massive parallelization on GPUs and ASICs. | Minimum 600,000 iterations (OWASP 2023) if used |
| **BCrypt** | Django, Ruby on Rails, OpenBSD, Spring Security | Passwords silently truncated at 72 bytes; not fully memory-hard. | **Recommended** (Cost $\ge 12$) |
| **Scrypt** | Litecoin mining, cryptocurrency wallets, Tarsnap | High memory requirements can exhaust web server RAM under high concurrency if misconfigured. | **Strong choice** ($N=16384, r=8, p=1$) |
| **Argon2id** | Bitwarden, KeePassXC, 1Password, modern web auth | Side-channel timing attacks on Argon2d; trade-off attacks on Argon2i; Argon2id balances both. | **Gold Standard (OWASP / IETF RFC 9106)** |
| **HKDF** | TLS 1.3 Key Schedule, Signal Protocol, WireGuard | None when used with SHA-256 or SHA-512; requires non-empty domain labels. | **Standard for Key Derivation** |

---

## 📂 Algorithm Index & Direct Modules

| Algorithm | Type / Standard | Memory-Hard? | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- | :--- |
| **PBKDF2** | RFC 2898 / NIST SP 800-132 | ❌ CPU-bound | [`kdf-algorithms/pbkdf2.py`](kdf-algorithms/pbkdf2.py) | `pbkdf2_menu` |
| **BCrypt** | Eksblowfish (OpenBSD) | ⚠️ Low memory | [`kdf-algorithms/bcrypt_module.py`](kdf-algorithms/bcrypt_module.py) | `bcrypt_menu` |
| **Scrypt** | RFC 7914 (Colin Percival) | ✅ Memory-hard | [`kdf-algorithms/scrypt_module.py`](kdf-algorithms/scrypt_module.py) | `scrypt_menu` |
| **Argon2** | RFC 9106 (PHC Winner) | ✅ Highly memory-hard | [`kdf-algorithms/argon2_module.py`](kdf-algorithms/argon2_module.py) | `argon2_menu` |
| **HKDF** | RFC 5869 Extract-and-Expand | ❌ Protocol KDF | [`kdf-algorithms/hkdf_module.py`](kdf-algorithms/hkdf_module.py) | `hkdf_menu` |

