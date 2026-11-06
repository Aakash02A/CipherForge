# 🔐 Level 02: Symmetric Key Cryptography

Welcome to **Level 02** of CipherForge. This level covers **symmetric key cryptography**, where communicating parties share a single secret key for both encryption and decryption. This level spans **Block Ciphers**, **Block Cipher Modes of Operation**, and **Stream Ciphers**.

---

## 🎯 Educational Objectives

- Differentiate between **Substitution-Permutation Networks (SPN)** (e.g. AES, Serpent, Kuznyechik) and **Feistel Networks** (e.g. DES, 3DES, Blowfish, Camellia).
- Understand Claude Shannon's foundational principles: **Confusion** (obscuring the relationship between key and ciphertext) and **Diffusion** (spreading plaintext statistics across the ciphertext).
- Analyze why **Electronic Codebook (ECB)** mode is catastrophic for confidentiality (the classic "ECB Penguin" phenomenon).
- Understand why stream ciphers and counter modes require **unique nonces/IVs** to prevent keystream reuse attacks.

---

## 🔬 Core Mathematical & Security Concepts

### 1. Substitution-Permutation Networks (SPN) vs. Feistel Networks
- **SPN (e.g. AES):** Invertible layers of S-Boxes (non-linear substitutions over Galois Fields $GF(2^8)$), ShiftRows, and MixColumns (linear diffusion over polynomials). Requires separate circuits for encryption and decryption.
- **Feistel Network (e.g. DES, Blowfish):** Splits state into left ($L_i$) and right ($R_i$) halves:
  $$L_{i+1} = R_i$$
  $$R_{i+1} = L_i \oplus F(R_i, K_i)$$
  Decryption is structurally identical to encryption, requiring only reversing the key schedule.

### 2. Block Cipher Modes of Operation
Block ciphers operate on fixed-size blocks (typically 64 or 128 bits). Modes of operation determine how arbitrary-length plaintexts are processed:

```text
[Plaintext Block 1]     [Plaintext Block 2]
         │                       │
         ▼                       ▼
    ┌─────────┐             ┌─────────┐
    │ Encrypt │             │ Encrypt │      <-- ECB Mode: Identical plaintext
    └─────────┘             └─────────┘          produces identical ciphertext!
         │                       │
         ▼                       ▼
[Ciphertext Block 1]    [Ciphertext Block 2]
```

- **ECB (Electronic Codebook):** Encrypts each block independently. Leaks statistical structure and patterns.
- **CBC (Cipher Block Chaining):** XORs each plaintext block with the previous ciphertext block:
  $$C_i = E_K(P_i \oplus C_{i-1}), \quad C_0 = \text{IV}$$
  Vulnerable to **Padding Oracle Attacks** (Vaudenay 2002) if decryption errors are leaked.
- **CTR (Counter Mode):** Converts a block cipher into a stream cipher by encrypting successive counter values:
  $$C_i = P_i \oplus E_K(\text{Nonce} \parallel i)$$
  Highly parallelizable, but reusing a `(Key, Nonce)` pair compromises security completely.
- **XTS (XEX Tweakable Block Cipher):** Designed specifically for storage disk encryption (IEEE 1619), mitigating data manipulation without ciphertext expansion.

### 3. Stream Ciphers & Keystream XOR
Stream ciphers generate a pseudorandom keystream $Z$ from a key $K$ and nonce $N$:
$$C = P \oplus Z(K, N)$$
$$\text{If } N_1 = N_2 \implies C_1 \oplus C_2 = (P_1 \oplus Z) \oplus (P_2 \oplus Z) = P_1 \oplus P_2$$
Two ciphertexts encrypted under the same key and nonce can be XORed together to completely cancel the keystream, allowing natural language crib-dragging attacks!

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm / Mode | Real-World Context | Vulnerabilities & Attacks | Modern Recommendation |
| :--- | :--- | :--- | :--- |
| **AES (Rijndael)** | Global industry standard (TLS, BitLocker, IPsec, SSH, WPA3) | Side-channel timing attacks on software table lookups (mitigated by AES-NI hardware instructions). | **Recommended** (AES-256 with GCM mode) |
| **DES** | US standard (1977); banking systems | 56-bit key space brute-forced in under 24 hours (EFF Deep Crack, 1998); 64-bit block size vulnerable to Sweet32. | **Deprecated / Insecure** |
| **3DES (Triple DES)** | Legacy ATM & financial PIN pads | Effective 112-bit key; Sweet32 collision attacks on 64-bit blocks after $2^{32}$ blocks. | **Deprecated** (NIST disallowed after 2023) |
| **Blowfish** | OpenBSD bcrypt, legacy OpenVPN | 64-bit block size vulnerable to Sweet32 birthday attacks on high-throughput connections. | Use **Twofish** or **AES** |
| **Twofish** | AES finalist, VeraCrypt disk encryption | Complex key schedule; slower software execution than AES, but uncompromised security. | **Secure alternative** to AES |
| **ECB Mode** | Inadvertently used by novice developers | Preserves identical patterns in ciphertext (leaks bitmap images, audio, repetitive JSON). | **Prohibited** in production |
| **CBC Mode** | TLS 1.2, legacy OpenVPN, PKCS#7 | Padding Oracle attacks (POODLE, Lucky Thirteen) unless combined with Encrypt-then-MAC. | Prefer AEAD (GCM / ChaCha20-Poly1305) |
| **RC4** | WEP, WPA-TKIP, SSL 3.0 / TLS 1.0 | Biased initial keystream bytes; Fluhrer-Mantin-Shamir (FMS) attack completely breaks WEP. | **Banned** (RFC 7465) |
| **ChaCha20** | TLS 1.3, Google Chrome, Android, WireGuard | None known when used with a 96-bit unique nonce; high performance on hardware lacking AES-NI. | **Recommended** (especially with Poly1305) |

---

## 📂 Algorithm Index & Direct Modules

### 2.1 Block Ciphers
| Algorithm | Key Sizes | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **AES** | 128, 192, 256 bits | [`block-ciphers/aes.py`](block-ciphers/aes.py) | `aes_menu` |
| **DES** | 56 bits | [`block-ciphers/des.py`](block-ciphers/des.py) | `des_menu` |
| **3DES** | 112, 168 bits | [`block-ciphers/des3.py`](block-ciphers/des3.py) | `des3_menu` |
| **Blowfish** | 32–448 bits | [`block-ciphers/blowfish.py`](block-ciphers/blowfish.py) | `blowfish_menu` |
| **Twofish** | 128, 192, 256 bits | [`block-ciphers/twofish.py`](block-ciphers/twofish.py) | `twofish_menu` |
| **IDEA** | 128 bits | [`block-ciphers/idea.py`](block-ciphers/idea.py) | `idea_menu` |
| **Camellia** | 128, 192, 256 bits | [`block-ciphers/camellia.py`](block-ciphers/camellia.py) | `camellia_menu` |
| **Serpent** | 128, 192, 256 bits | [`block-ciphers/serpent.py`](block-ciphers/serpent.py) | `serpent_menu` |
| **RC5** | Variable | [`block-ciphers/rc5.py`](block-ciphers/rc5.py) | `rc5_menu` |
| **RC6** | 128, 192, 256 bits | [`block-ciphers/rc6.py`](block-ciphers/rc6.py) | `rc6_menu` |
| **Magma** | 256 bits (GOST) | [`block-ciphers/magma.py`](block-ciphers/magma.py) | `magma_menu` |
| **Kuznyechik** | 256 bits (GOST) | [`block-ciphers/kuznyechik.py`](block-ciphers/kuznyechik.py) | `kuznyechik_menu` |

### 2.2 Block Cipher Modes
| Mode | Full Name | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **ECB** | Electronic Codebook | [`cipher-modes/Ecb.py`](cipher-modes/Ecb.py) | `ecb_menu` |
| **CBC** | Cipher Block Chaining | [`cipher-modes/Cbc.py`](cipher-modes/Cbc.py) | `cbc_menu` |
| **CFB** | Cipher Feedback | [`cipher-modes/Cfb.py`](cipher-modes/Cfb.py) | `cfb_menu` |
| **OFB** | Output Feedback | [`cipher-modes/Ofb.py`](cipher-modes/Ofb.py) | `ofb_menu` |
| **CTR** | Counter Mode | [`cipher-modes/Ctr.py`](cipher-modes/Ctr.py) | `ctr_menu` |
| **GCM** | Galois/Counter Mode | [`cipher-modes/Gcm.py`](cipher-modes/Gcm.py) | `gcm_menu` |
| **CCM** | Counter with CBC-MAC | [`cipher-modes/Ccm.py`](cipher-modes/Ccm.py) | `ccm_menu` |
| **XTS** | XEX Tweakable Codebook | [`cipher-modes/Xts.py`](cipher-modes/Xts.py) | `xts_menu` |

### 2.3 Stream Ciphers
| Algorithm | Design Profile | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **ChaCha20** | RFC 8439 Modern Standard | [`stream-ciphers/Chacha20.py`](stream-ciphers/Chacha20.py) | `chacha20_menu` |
| **Salsa20** | eSTREAM Portfolio | [`stream-ciphers/Salsa20.py`](stream-ciphers/Salsa20.py) | `salsa20_menu` |
| **RC4** | Legacy Ron's Code 4 | [`stream-ciphers/Rc4.py`](stream-ciphers/Rc4.py) | `rc4_menu` |
| **HC-128** | eSTREAM Software Profile | [`stream-ciphers/Hc128.py`](stream-ciphers/Hc128.py) | `hc128_menu` |
| **Rabbit** | eSTREAM 128-bit High-speed | [`stream-ciphers/Rabbit.py`](stream-ciphers/Rabbit.py) | `rabbit_menu` |
| **A5/1** | GSM Cellular Stream Cipher | [`stream-ciphers/A51.py`](stream-ciphers/A51.py) | `a51_menu` |

