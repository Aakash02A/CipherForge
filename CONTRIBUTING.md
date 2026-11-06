# Contributing to CipherForge

Thank you for your interest in contributing to **CipherForge**! We are building the premier community-driven educational repository for understanding cryptography algorithms, security engineering, and cryptanalysis.

> [!NOTE]
> CipherForge is strictly dedicated to **pedagogical education, mathematical exposition, and transparent security research**. We celebrate runnable demonstrations of *broken* algorithms (to teach why they failed) alongside modern cryptographic standards.

---

## 🌟 Good First Issues for New Contributors

If you want to contribute but don't know where to start, here are ideal introductory opportunities:

### 1. 🧪 Unit Tests & RFC Test Vectors
- Add automated pytest test cases in `tests/` verifying algorithms against official NIST CAVP / RFC test vectors (e.g. RFC 8439 ChaCha20 test vectors, NIST FIPS 197 AES KAT vectors).
- Add edge-case test suites (empty strings, huge messages, non-ASCII Unicode characters).

### 2. 🔬 Cryptanalysis & Attack Simulations
- **Padding Oracle Attack:** Create a demonstration in Level 02 showing how a CBC padding oracle reveals plaintext byte-by-byte.
- **Length Extension Attack:** Demonstrate length extension on SHA-256 vs. failure on SHA-3 and HMAC in Level 04.
- **Birthday Paradox Visualizer:** Script demonstrating collision probabilities across 16-bit to 64-bit truncated hashes.
- **Nonce-Reuse Attack Script:** Demonstrate how reusing a nonce in AES-GCM recovers the internal $H$ authentication key.

### 3. ⏱️ Big-O Complexity & Benchmarking Notes
- Add computational time and space complexity tables in level documentation.
- Build benchmark scripts measuring throughput (MB/s) for symmetric block ciphers and stream ciphers.

### 4. 🎨 Visualizations & Markdown Diagrams
- Add ASCII or Mermaid architecture diagrams illustrating cipher internal round operations, Feistel steps, or key schedules.

---

## 🛠️ Setting Up Your Local Environment

```bash
# 1. Fork the repo on GitHub and clone your fork locally:
git clone https://github.com/YOUR_USERNAME/CipherForge.git
cd CipherForge

# 2. Create and activate a Python virtual environment:
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

# 3. Install required and development dependencies:
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov

# 4. Verify that all 90 modules pass diagnostics:
python -c "import main, sys; ok, fail = main.run_diagnostics(pause=False); sys.exit(fail)"
```

---

## 📁 Repository Level Architecture

Modules are organized into 8 progressive learning levels:

```text
CipherForge/
├── level-01-classical-ciphers/        # Caesar, Vigenère, Playfair, Hill, Enigma, Rail Fence
├── level-02-symmetric-crypto/         # Block ciphers, cipher modes (ECB, CBC, GCM), Stream ciphers
├── level-03-asymmetric-crypto/        # RSA, ElGamal, Diffie-Hellman, ECDH, X25519, Curves
├── level-04-hashing-and-macs/         # SHA-2, SHA-3, BLAKE3, HMAC, Poly1305, AEAD (GCM/CCM/OCB)
├── level-05-signatures-and-protocols/ # ECDSA, Ed25519, Schnorr, TLS 1.3, SSH-2, IPsec, PGP, Kerberos
├── level-06-password-and-kdf/         # PBKDF2, BCrypt, Scrypt, Argon2id, HKDF
├── level-07-advanced-and-pqc/         # Kyber, Dilithium, Falcon, SPHINCS+, FHE, Secret Sharing, ZKPs
└── level-08-capstone-project/         # SecureVault CLI & E2EE Messaging application
```

---

## 📝 Coding Standards & Module Guidelines

When adding a new module or modifying an existing one:

1. **Self-Contained & Clear:** Keep educational algorithm files clean and self-explanatory. Include mathematical docstrings citing RFCs or academic papers.
2. **Standard Menu Interface:** If adding an interactive module, expose a `{name}_menu()` entry point following the repo's input pattern.
3. **Register in `main.py`:** Add your module path and menu function to `_ALL_MODULES` in `main.py` and register it in the appropriate level submenu.
4. **No Secrets or Real Keys:** Never commit production certificates, real API keys, or private passwords.
5. **Constant-Time Comparison:** Use `secrets.compare_digest()` or `hmac.compare_digest()` when validating hashes, tokens, or MAC tags.

---

## 🧪 Testing Guidelines

Always run the test suite before submitting a Pull Request:

```bash
# Run all unit tests
pytest tests/ -v

# Run module import diagnostics
python -c "import main, sys; ok, fail = main.run_diagnostics(pause=False); sys.exit(fail)"
```

---

## 🔀 Git Workflow & Pull Request Process

1. **Branch Naming:** Create a descriptive branch:
   - `feat/argon2-benchmarks`
   - `fix/hill-cipher-inverse`
   - `docs/rsa-padding-explanation`
   - `test/chacha20-rfc-vectors`
2. **Commit Messages:** Use conventional, structured commits:
   - `feat(level-06): add Argon2id cost factor benchmark`
   - `test(level-02): add NIST test vectors for AES-GCM`
   - `docs(level-03): clarify Bleichenbacher padding attack math`
3. **Submit PR:** Open a Pull Request on GitHub using our template. Ensure CI checks pass.

Thank you for helping make cryptography accessible, mathematically rigorous, and fun to learn! 🔐
