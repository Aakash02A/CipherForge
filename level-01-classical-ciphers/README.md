# 📜 Level 01: Classical & Historical Ciphers

Welcome to **Level 01** of CipherForge. This level establishes foundational cryptographic concepts through the study of historical pen-and-paper ciphers, substitution, transposition, polyalphabetic mechanisms, and electro-mechanical rotor machines.

---

## 🎯 Educational Objectives

- Understand the mathematical differences between **substitution ciphers** (replacing characters) and **transposition ciphers** (permuting character positions).
- Learn how statistical properties of natural language (letter frequency, digraphs, trigraphs) survive simple encryption.
- Master cryptanalysis techniques: brute force key search, index of coincidence, the Kasiski test, and frequency analysis.
- Understand the evolution from simple monoalphabetic substitution to polyalphabetic ciphers and machine rotors.

---

## 🔬 Core Mathematical & Security Concepts

### 1. Modular Arithmetic over Finite Alphabets
Classical ciphers operate over the ring of integers modulo 26 ($\mathbb{Z}_{26}$):
$$\text{Enc}(m) = (m + k) \pmod{26}$$
$$\text{Dec}(c) = (c - k) \pmod{26}$$

### 2. Polyalphabetic Substitution
While monoalphabetic ciphers preserve single-letter frequencies ($P(\text{'E'}) \approx 12.7\%$), the Vigenère cipher shifts characters using a repeating keyword of length $L$:
$$c_i = (m_i + k_{i \pmod L}) \pmod{26}$$
This flattens the frequency distribution, but repeats patterns every $L$ characters, allowing the **Kasiski examination** and **Friedman index of coincidence** to recover key length.

### 3. Matrix Transformations & Linear Algebra (Hill Cipher)
The Hill cipher encrypts blocks of $n$ letters using matrix multiplication over $\mathbb{Z}_{26}$:
$$\mathbf{c} = K \cdot \mathbf{m} \pmod{26}$$
Decryption requires finding the modular inverse matrix $K^{-1} \pmod{26}$, which exists if and only if:
$$\gcd(\det(K), 26) = 1$$

### 4. Rotor Permutations & Reciprocal Reflection (Enigma Machine)
The German Enigma machine combines multiple stepping rotors with a plugboard (*Steckerbrett*) and a reflector (*Umkehrwalze*). The reflector ensures that encryption is reciprocal ($\text{Enc}(\text{Enc}(x)) = x$), but introduces a fatal mathematical flaw: **a letter could never encrypt to itself**.

---

## ⚖️ Real-World Use Cases vs. Known Vulnerabilities

| Algorithm | Historical / Modern Context | Critical Vulnerabilities & Attacks | Why It's Deprecated Today |
| :--- | :--- | :--- | :--- |
| **Caesar Cipher** | Roman military communications (Julius Caesar, ~58 BC) | Tiny key space ($|\mathcal{K}| = 25$); broken by brute force in milliseconds or frequency analysis. | Trivial single-operation substitution. |
| **Vigenère Cipher** | 16th-century diplomatic secret correspondence ("le chiffre indéchiffrable") | Kasiski examination and Index of Coincidence identify key period $L$; individual alphabets broken by frequency analysis. | Periodic key reuse leaks statistical information. |
| **Playfair Cipher** | Boer War and WWI battlefield tactical tactical telegraphy | 5×5 matrix digraph substitution lacks single-letter frequency, but reverse digraphs and matrix alignment can be deduced from 600 words of ciphertext. | Digraph frequency remains non-uniform. |
| **Hill Cipher** | First practical polygraphic algebraic cipher (Lester S. Hill, 1929) | Completely broken by a **Known-Plaintext Attack (KPA)** using simple Gaussian elimination modulo 26 with $n$ plaintext-ciphertext vector pairs. | Linear algebraic vulnerability to known plaintext. |
| **Enigma Machine** | WWII German military command and naval communications | Known plaintext ("cribs"), improper operator habits, absence of self-encryption ($E(x) \neq x$), cracked at Bletchley Park via Bombe machines. | Fixed rotor wirings and lack of non-linear diffusion. |
| **Rail Fence** | Civil War tactical message scrambling | Pure transposition preserves letter frequency identically; key space equals text length; easily reconstructed by anagramming. | No diffusion or substitution confusion. |

---

## 📂 Algorithm Index & Direct Modules

| Algorithm | Type | Implementation Path | CLI Function |
| :--- | :--- | :--- | :--- |
| **Caesar Cipher** | Monoalphabetic Substitution | [`traditional-ciphers/Caesar.py`](traditional-ciphers/Caesar.py) | `caesar_menu` |
| **Vigenère Cipher** | Polyalphabetic Substitution | [`traditional-ciphers/Vigenere.py`](traditional-ciphers/Vigenere.py) | `vigenere_menu` |
| **Playfair Cipher** | Digraphic Substitution | [`traditional-ciphers/Playfair.py`](traditional-ciphers/Playfair.py) | `playfair_menu` |
| **Hill Cipher** | Polygraphic Linear Algebraic | [`traditional-ciphers/Hill.py`](traditional-ciphers/Hill.py) | `hill_menu` |
| **Enigma Machine** | Polyalphabetic Rotor Machine | [`traditional-ciphers/Enigma.py`](traditional-ciphers/Enigma.py) | `enigma_menu` |
| **Rail Fence Cipher** | Geometric Transposition | [`traditional-ciphers/rail_fence.py`](traditional-ciphers/rail_fence.py) | `rail_fence_menu` |

---

## 🧪 Hands-On Cryptanalysis Exercises

1. **Caesar Brute Force:** Run `python -m level-01-classical-ciphers.traditional-ciphers.Caesar` and encrypt a secret with shift 19. Run the frequency analysis option to observe the shifted frequency peak.
2. **Hill Matrix Inversion:** Try encrypting a 2-character block with an invalid matrix (where $\det(K)$ shares a factor with 26) and note why the system rejects non-invertible matrices.
3. **Enigma Self-Encryption Test:** Verify empirically that an Enigma encryption never outputs the original letter at any position.

