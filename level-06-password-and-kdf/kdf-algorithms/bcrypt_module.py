import os
import time

try:
    import bcrypt
    _BCRYPT_AVAILABLE = True
except ImportError:
    _BCRYPT_AVAILABLE = False


def _save_output(content: str, filename: str = "bcrypt_output.txt") -> None:
    os.makedirs("samples", exist_ok=True)
    path = os.path.join("samples", filename)
    try:
        with open(path, "w") as f:
            f.write(content)
        print(f"  [Saved] → {path}")
    except OSError as e:
        print(f"  [Error] Failed to save file: {e}")


def hash_password_demo() -> None:
    print("\n--- BCrypt Password Hashing ---")
    if not _BCRYPT_AVAILABLE:
        print("  [Error] bcrypt library not installed. Run: pip install bcrypt")
        return

    password = input("  Enter password to hash: ").strip()
    if not password:
        print("  [Error] Password cannot be empty.")
        return

    cost_str = input("  Enter work factor / cost [4-16, default 12]: ").strip()
    cost = int(cost_str) if cost_str.isdigit() and 4 <= int(cost_str) <= 16 else 12

    print(f"\n  Hashing with cost factor 2^{cost} ({1 << cost} iterations)...")
    salt = bcrypt.gensalt(rounds=cost)
    t0 = time.perf_counter()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    ms = (time.perf_counter() - t0) * 1000

    hashed_text = hashed.decode("utf-8")
    print(f"\n  [Success] Hashed in {ms:.2f} ms")
    print(f"  BCrypt Hash String: {hashed_text}")
    print(f"    - Identifier  : {hashed_text[:3]}")
    print(f"    - Cost factor : {hashed_text[4:6]}")
    print(f"    - Salt & Hash : {hashed_text[7:]}")

    save = input("\n  Save hash output? (y/n): ").strip().lower()
    if save == "y":
        out = (
            f"BCrypt Hash Output\n"
            f"------------------\n"
            f"Cost Factor : {cost}\n"
            f"Hash String : {hashed_text}\n"
        )
        _save_output(out, "bcrypt_output.txt")


def verify_password_demo() -> None:
    print("\n--- BCrypt Password Verification ---")
    if not _BCRYPT_AVAILABLE:
        print("  [Error] bcrypt library not installed. Run: pip install bcrypt")
        return

    password = input("  Create password: ").strip()
    if not password:
        return

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10))
    print(f"  Hashed reference stored: {hashed.decode('utf-8')[:30]}...")

    attempt = input("\n  Enter password to verify: ").strip()
    t0 = time.perf_counter()
    matches = bcrypt.checkpw(attempt.encode("utf-8"), hashed)
    ms = (time.perf_counter() - t0) * 1000

    if matches:
        print(f"  ✅ [PASS] Password matched! Verified in {ms:.2f} ms")
    else:
        print(f"  ❌ [FAIL] Password mismatch! Verified in {ms:.2f} ms")


def benchmark_cost_factors() -> None:
    print("\n--- BCrypt Cost Factor Timing Benchmark ---")
    if not _BCRYPT_AVAILABLE:
        print("  [Error] bcrypt library not installed. Run: pip install bcrypt")
        return

    password = b"benchmark-secret-password-123"
    print("  Measuring latency per cost factor (2^cost rounds):\n")
    print(f"  {'Cost':<6} | {'Rounds':<10} | {'Duration (ms)':<15} | {'Suitability'}")
    print(f"  {'-'*6}-+-{'-'*10}-+-{'-'*15}-+-{'-'*20}")

    for cost in [8, 9, 10, 11, 12, 13]:
        t0 = time.perf_counter()
        salt = bcrypt.gensalt(rounds=cost)
        bcrypt.hashpw(password, salt)
        ms = (time.perf_counter() - t0) * 1000

        suitability = "Fast / Dev Only" if cost < 10 else ("Acceptable" if cost <= 12 else "Strong / Interactive")
        print(f"  {cost:<6} | {1 << cost:<10} | {ms:<15.2f} | {suitability}")


def show_how_bcrypt_works() -> None:
    print("\n--- How BCrypt Works ---")
    print("""
  BCrypt was designed in 1999 by Niels Provos and David Mazières for OpenBSD,
  based on the Blowfish symmetric cipher (specifically 'Eksblowfish' - 
  Expensive Key Schedule Blowfish).

  Key Innovations:
    1. Adaptive Work Factor: The cost parameter defines the number of rounds (2^cost).
       As hardware accelerates, the cost factor can be increased without altering
       the underlying algorithm.
    2. Salt Embedded: BCrypt formats include the version ($2a$, $2b$), the cost,
       the 128-bit salt, and the 184-bit hash in a standard 60-character modular string:
       $2b$12$e8x/kM...

  Limitations:
    - Maximum password length is truncated at 72 bytes due to Blowfish design.
    - Not fully memory-hard compared to Scrypt or Argon2, though far more
      resistant to GPU parallelization than PBKDF2 or raw SHA-256.
    """)


def bcrypt_menu() -> None:
    while True:
        print("\n--- BCrypt Password Hashing ---")
        print("  Category: Password Hashing & Key Derivation (Level 06)")
        print("  Algorithm: Eksblowfish-based Adaptive Hashing")
        print()
        print("  1. Hash Password with Custom Cost Factor")
        print("  2. Verify Password against BCrypt Hash")
        print("  3. Benchmark Cost Factor Latency (2^rounds)")
        print("  4. How BCrypt Works")
        print("  5. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            hash_password_demo()
        elif choice == "2":
            verify_password_demo()
        elif choice == "3":
            benchmark_cost_factors()
        elif choice == "4":
            show_how_bcrypt_works()
        elif choice == "5":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–5.")

