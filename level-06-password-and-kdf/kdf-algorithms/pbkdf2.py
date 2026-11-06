import os
import hashlib
import secrets
import time

# ── helpers ───────────────────────────────────────────────────────────────────

def _save_output(content: str, filename: str = "pbkdf2_output.txt") -> None:
    os.makedirs("samples", exist_ok=True)
    path = os.path.join("samples", filename)
    try:
        with open(path, "w") as f:
            f.write(content)
        print(f"  [Saved] → {path}")
    except OSError as e:
        print(f"  [Error] Failed to save file: {e}")


# ── core functions ────────────────────────────────────────────────────────────

def derive_key_demo() -> None:
    print("\n--- PBKDF2 Key Derivation ---")
    password = input("  Enter password: ").strip()
    if not password:
        print("  [Error] Password cannot be empty.")
        return

    iter_input = input("  Enter iteration count (default 600,000 as per OWASP): ").strip()
    iterations = int(iter_input) if iter_input.isdigit() and int(iter_input) > 0 else 600000

    hash_choice = input("  Hash algorithm [1=SHA256 (default), 2=SHA512]: ").strip()
    hash_name = "sha512" if hash_choice == "2" else "sha256"

    key_len_input = input("  Key length in bytes (default 32): ").strip()
    dklen = int(key_len_input) if key_len_input.isdigit() and int(key_len_input) > 0 else 32

    # Generate a cryptographically secure 16-byte salt
    salt = secrets.token_bytes(16)

    print(f"\n  Deriving key using PBKDF2-HMAC-{hash_name.upper()}...")
    t0 = time.perf_counter()
    derived_key = hashlib.pbkdf2_hmac(
        hash_name,
        password.encode("utf-8"),
        salt,
        iterations,
        dklen=dklen
    )
    elapsed = time.perf_counter() - t0

    print(f"\n  [Success] Key derived in {elapsed * 1000:.2f} ms")
    print(f"  Salt (hex)         : {salt.hex()}")
    print(f"  Iterations         : {iterations:,}")
    print(f"  Derived Key (hex)  : {derived_key.hex()}")
    print(f"  Key Length         : {len(derived_key)} bytes ({len(derived_key)*8} bits)")

    save = input("\n  Save derivation output? (y/n): ").strip().lower()
    if save == "y":
        out = (
            f"PBKDF2 Derivation Result\n"
            f"------------------------\n"
            f"Algorithm  : PBKDF2-HMAC-{hash_name.upper()}\n"
            f"Iterations : {iterations}\n"
            f"Salt (hex) : {salt.hex()}\n"
            f"Key (hex)  : {derived_key.hex()}\n"
        )
        _save_output(out, "pbkdf2_output.txt")


def benchmark_iterations() -> None:
    print("\n--- PBKDF2 Iteration Benchmark ---")
    password = b"benchmark-secret-password-123"
    salt = b"benchmark_salt16"
    test_counts = [10000, 50000, 100000, 300000, 600000]

    print(f"  Benchmarking PBKDF2-HMAC-SHA256 across iteration counts:\n")
    print(f"  {'Iterations':<15} | {'Duration (ms)':<15} | {'NIST / OWASP Status'}")
    print(f"  {'-'*15}-+-{'-'*15}-+-{'-'*25}")

    for count in test_counts:
        t0 = time.perf_counter()
        hashlib.pbkdf2_hmac("sha256", password, salt, count, dklen=32)
        ms = (time.perf_counter() - t0) * 1000

        status = "Legacy (Weak)" if count < 100000 else ("Acceptable" if count < 600000 else "OWASP Recommended")
        print(f"  {count:<15,} | {ms:<15.2f} | {status}")


def verify_password_demo() -> None:
    print("\n--- PBKDF2 Password Verification ---")
    password = input("  Set a password to store: ").strip()
    if not password:
        return

    salt = secrets.token_bytes(16)
    iterations = 300000
    stored_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations, 32)
    print(f"  Password hashed and stored with salt: {salt.hex()[:16]}...")

    attempt = input("\n  Enter password to verify: ").strip()
    test_hash = hashlib.pbkdf2_hmac("sha256", attempt.encode(), salt, iterations, 32)

    # Use secrets.compare_digest for constant-time comparison
    if secrets.compare_digest(stored_hash, test_hash):
        print("  ✅ [PASS] Password verified successfully (constant-time match).")
    else:
        print("  ❌ [FAIL] Incorrect password! Hashes do not match.")


def show_how_pbkdf2_works() -> None:
    print("\n--- How PBKDF2 Works ---")
    print("""
  PBKDF2 (Password-Based Key Derivation Function 2 - RFC 2898 / NIST SP 800-132)
  is designed to make brute-force and dictionary attacks computationally expensive.

  Core Algorithm:
    DK = PBKDF2(PRF, Password, Salt, c, dkLen)

    1. Uses a Pseudorandom Function (PRF), typically HMAC-SHA256 or HMAC-SHA512.
    2. Salt (minimum 128-bit) prevents precomputed rainbow table attacks.
    3. Iteration count 'c' repeatedly chains the PRF:
       U_1 = PRF(Password, Salt || INT_32_BE(i))
       U_2 = PRF(Password, U_1)
       ...
       U_c = PRF(Password, U_{c-1})
       F = U_1 XOR U_2 XOR ... XOR U_c

  Security Considerations:
    - CPU Bound: PBKDF2 requires very little memory, making it vulnerable to
      massively parallel GPU / ASIC attacks compared to memory-hard schemes.
    - Recommended for symmetric key derivation (e.g. deriving an AES key from
      a user passphrase) when combined with high iteration counts (>= 600,000).
    """)


# ── menu ──────────────────────────────────────────────────────────────────────

def pbkdf2_menu() -> None:
    while True:
        print("\n--- PBKDF2 (Password-Based Key Derivation Function 2) ---")
        print("  Category: Password Hashing & Key Derivation (Level 06)")
        print("  Standard: RFC 2898 / NIST SP 800-132")
        print()
        print("  1. Derive Encryption Key from Password")
        print("  2. Benchmark Iteration Counts (Timing Analysis)")
        print("  3. Password Hashing & Verification Demo")
        print("  4. How PBKDF2 Works")
        print("  5. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            derive_key_demo()
        elif choice == "2":
            benchmark_iterations()
        elif choice == "3":
            verify_password_demo()
        elif choice == "4":
            show_how_pbkdf2_works()
        elif choice == "5":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–5.")

