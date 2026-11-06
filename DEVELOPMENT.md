# Development Guide

Quick reference for developers contributing to the **CipherForge** cryptography learning toolkit.

## 🏗️ Architecture Overview

### Main Entry Point
- **`main.py`** — interactive CLI menu dispatcher and package router
- Handles user input and delegates to the algorithm modules for each learning level
- Uses a safe `importlib`-based import wrapper to gracefully handle missing modules and dependencies

### Module Organization
The toolkit is organised into **8 progressive learning levels**. Each level is a
top-level package that groups algorithms into sub-category folders:

```
level-01-classical-ciphers/
└── traditional-ciphers/          Caesar.py, Vigenere.py, Playfair.py, Hill.py, Enigma.py, rail_fence.py

level-02-symmetric-crypto/
├── block-ciphers/                aes.py, des.py, des3.py, blowfish.py, twofish.py, ...
├── cipher-modes/                 Ecb.py, Cbc.py, Ctr.py, Gcm.py, ...
└── stream-ciphers/               Chacha20.py, Salsa20.py, Rc4.py, ...

level-03-asymmetric-crypto/       public-key-encryption/, key-exchange/, elliptic-curves/
level-04-hashing-and-macs/        hash-functions/, message-authentication/, authenticated-encryption/
level-05-signatures-and-protocols/ digital-signatures/, protocols/
level-06-password-and-kdf/        kdf-algorithms/
level-07-advanced-and-pqc/        post-quantum-kems/, post-quantum-signatures/, homomorphic-encryption/, secret-sharing/, secure-computation/, zero-knowledge-proofs/
level-08-capstone-project/        secure_vault.py, v1-early-prototype/
```

Every directory in a module path contains an `__init__.py` package marker, and each
category folder ships a `README.md` documenting the algorithms it contains.

> [!IMPORTANT]
> **Hyphenated folder names are not valid Python identifiers**, so you cannot use
> plain `import` or `from ... import` statements against them. All modules are loaded
> dynamically with `importlib.import_module(...)`, which maps each dotted segment to a
> filesystem path and works fine with hyphens. Always reference modules using that
> dotted-path string form — e.g. `"level-02-symmetric-crypto.block-ciphers.aes"` — exactly
> as `main.py` does.

### Key Functions in `main.py`

| Function | Purpose |
|----------|---------|
| `_load()` / `_import()` | Safe `importlib`-based module load with error capture |
| `_run()` | Execute an algorithm menu with graceful fallback |
| `_get_choice()` | Read user input safely |
| `_clear()` / `_header()` / `_sub_header()` / `_menu_item()` | OS-aware display helpers |
| `menu_classical()` … `menu_capstone()` | Per-level menu dispatchers (Levels 01–08) |
| `run_diagnostics()` | Verify that all 90 registered modules import cleanly |
| `show_setup_guide()` | Print environment / dependency setup instructions |
| `_ALL_MODULES` | Registry list `(dotted_module_path, menu_function_name)` used by diagnostics |

## 📚 Algorithm Module Template

Every algorithm module **must** expose a single zero-argument entry-point function named
`<algorithm>_menu()` so the CLI and the diagnostics registry can call it uniformly:

```python
"""
Algorithm Name Module
Level: 02 — Symmetric Key Cryptography

Implements: [Algorithm description]
Standard:   [RFC / NIST / Academic reference]
Type:       [Block Cipher / Hash / Signature / KDF / etc.]
"""

def algorithm_menu() -> None:
    """Interactive menu — the single entry-point used by main.py and diagnostics."""
    while True:
        # Display options
        # Read user choice
        # Perform the cryptographic operation
        # Handle back / exit
        pass

# --- Helpers (private, prefixed with underscore) ---
def _generate_key() -> bytes:
    """Generate a cryptographic key using the `secrets` module."""
    ...

def _operation(data: bytes, key: bytes) -> bytes:
    """Perform the cryptographic operation."""
    ...

if __name__ == "__main__":
    algorithm_menu()
```

## 🔧 Development Workflow

### 1. Create a New Algorithm
```bash
# Add the module inside the matching level / sub-category folder, e.g.:
#   level-02-symmetric-crypto/block-ciphers/algorithm.py
# (Windows PowerShell: New-Item level-02-symmetric-crypto/block-ciphers/algorithm.py)
touch level-02-symmetric-crypto/block-ciphers/algorithm.py

# Implement it and expose an `algorithm_menu()` entry-point.
# Add a menu option to the matching menu function in main.py (e.g. menu_symmetric()).
# Register the dotted path in the _ALL_MODULES list.
```

### 2. Test Your Changes
```bash
# Check syntax
python -m py_compile level-02-symmetric-crypto/block-ciphers/algorithm.py

# Test the dynamic import used by the CLI (note the hyphenated dotted path)
python -c "import importlib; importlib.import_module('level-02-symmetric-crypto.block-ciphers.algorithm')"

# Run the affected level's automated tests
pytest tests/test_level_02_symmetric.py -v

# Launch the full toolkit
python main.py
```

### 3. Verify Integration
```bash
python main.py     # navigate to your level, select your algorithm, exercise every menu option
python -c "import main; ok, fail = main.run_diagnostics(pause=False); raise SystemExit(fail)"
```

## 📦 Dependencies

Core libraries are pinned in `requirements.txt`:

### Required
- `cryptography >= 42.0.0` — modern primitives, AEAD, ECC
- `pycryptodome >= 3.20.0` — legacy algorithm implementations (AES, DES, RSA, …)
- `blake3 >= 1.0.0` — BLAKE3 hashing (Level 04)
- `bcrypt >= 4.1.0` — BCrypt password hashing (Level 06)
- `argon2-cffi >= 23.1.0` — Argon2 password hashing (Level 06)
- `pytest >= 8.0.0` — test framework

### Optional (graceful fallback if not installed)
- `twofish` — Twofish block cipher
- `tiger` — Tiger hash (needs C++ build tools on Windows)
- `whirlpool` — Whirlpool hash (needs C++ build tools on Windows)

### Importing
```python
# Preferred: use the cryptography library
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Fallback: use pycryptodome
from Crypto.Cipher import AES

# Pure Python: use the standard library
import hashlib, hmac, secrets
```

## 🎨 Code Style

### Naming
- Functions: `snake_case` (e.g. `generate_key()`, `aes_menu()`)
- Classes: `PascalCase` (e.g. `CipherMode`)
- Constants: `UPPER_CASE` (e.g. `BLOCK_SIZE = 128`)

### Documentation
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief one-line description.

    Longer description if needed — explain behaviour and edge cases.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of the return value

    Raises:
        ValueError: When X happens
    """
```

### Error Handling
```python
try:
    result = perform_operation(input_data)
    print(f"  ✅ Success: {result}")
except ValueError as e:
    print(f"  ❌ Invalid input: {e}")
except Exception as e:
    print(f"  ❌ Unexpected error: {e}")
```

## 🧪 Testing Checklist

Before submitting a PR, verify:

- [ ] Module imports without errors (via `importlib`, since folder names contain hyphens)
- [ ] The entry-point is named exactly `<algorithm>_menu()` and takes no arguments
- [ ] All menu options run without crashing
- [ ] Error messages are user-friendly
- [ ] Back / exit options return to the parent menu
- [ ] Type hints on all functions, docstrings on public ones
- [ ] No hardcoded absolute paths or OS-specific system dependencies
- [ ] Works on Windows, Linux, and macOS
- [ ] Added a case to the matching `tests/test_level_XX_*.py` file
- [ ] `pytest` passes and `python main.py` diagnostics report 0 failures

Run the whole suite locally:
```bash
pytest -q
```

## 📊 Module Statistics

- **Registered Modules:** 90
- **Learning Levels:** 8
- **Python Files:** 100+
- **Automated Tests:** 23 across all 8 levels (`pytest`)
- **Python Version:** 3.10+ (3.11+ recommended)

## 🐛 Debugging Tips

### Import Errors
```bash
# Test the dynamic import used by the CLI
python -c "import importlib; importlib.import_module('level-02-symmetric-crypto.block-ciphers.algorithm')"

# Ensure an __init__.py package marker exists in every folder along the dotted path
ls level-02-symmetric-crypto/__init__.py level-02-symmetric-crypto/block-ciphers/__init__.py

# Verify the file compiles
python -m py_compile level-02-symmetric-crypto/block-ciphers/algorithm.py
```

### Menu Issues
```bash
python main.py   # navigate and inspect output

# Call a menu function directly
python -c "import importlib as i; m = i.import_module('level-02-symmetric-crypto.block-ciphers.algorithm'); m.algorithm_menu()"
```

### Dependency Issues
```bash
pip list | grep -Ei "cryptography|pycryptodome|blake3|bcrypt|argon2"
pip install -r requirements.txt --force-reinstall
```

## 🔐 Security Considerations

- **Randomness:** use the `secrets` module for keys, IVs, and nonces
- **Input validation:** always validate and bound user input
- **Error messages:** never leak sensitive material
- **Dependencies:** keep to the latest stable versions
- **Standards:** follow NIST and RFC guidance
- **Educational scope:** implementations are for learning, **not** production protection

## 📝 Common Tasks

### Add a New Sub-Category Folder
```bash
mkdir -p level-02-symmetric-crypto/new-subcategory
touch level-02-symmetric-crypto/new-subcategory/__init__.py
# also add a README.md describing the sub-category
```

### Register an Algorithm in `main.py`
```python
# 1) Add an option inside the matching level menu function, e.g. menu_symmetric():
elif c == "1":
    _run("level-02-symmetric-crypto.block-ciphers.algorithm",
         "algorithm_menu", "Algorithm Name")

# 2) Add it to the _ALL_MODULES registry (used by the D diagnostics command):
_ALL_MODULES = [
    ("level-02-symmetric-crypto.block-ciphers.algorithm", "algorithm_menu"),
    # ...
]
```

## 🤝 Getting Help

- **Code questions:** open a GitHub Discussion
- **Bug reports:** file an Issue using the bug-report template
- **New algorithm ideas:** use the "New Algorithm Request" issue template
- **Contribution workflow:** read [CONTRIBUTING.md](CONTRIBUTING.md)

## 📚 Resources

- **Cryptography Library:** https://cryptography.io/
- **PyCryptodome:** https://pycryptodome.readthedocs.io/
- **NIST Standards:** https://www.nist.gov/
- **RFC Standards:** https://www.ietf.org/rfc/

---

Happy coding! 🚀 If you have questions, feel free to ask in Discussions or Issues.
