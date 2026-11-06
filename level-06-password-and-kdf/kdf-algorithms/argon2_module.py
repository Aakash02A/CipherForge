import os
import time

try:
    from argon2 import PasswordHasher, Type
    from argon2.exceptions import VerifyMismatchError
    _ARGON2_AVAILABLE = True
except ImportError:
    _ARGON2_AVAILABLE = False


def _save_output(content: str, filename: str = "argon2_output.txt") -> None:
    os.makedirs("samples", exist_ok=True)
    path = os.path.join("samples", filename)
    try:
        with open(path, "w") as f:
            f.write(content)
        print(f"  [Saved] → {path}")
    except OSError as e:
        print(f"  [Error] Failed to save file: {e}")


def hash_password_demo() -> None:
    print("\n--- Argon2 Password Hashing (PHC Winner - RFC 9106) ---")
    if not _ARGON2_AVAILABLE:
        print("  [Error] argon2-cffi not installed. Run: pip install argon2-cffi")
        return

    password = input("  Enter password to hash: ").strip()
    if not password:
        print("  [Error] Password cannot be empty.")
        return

    print("\n  Select Argon2 Variant:")
    print("    1. Argon2id (Hybrid - OWASP / IETF Recommended)")
    print("    2. Argon2i  (Data-independent - optimized against side-channel attacks)")
    print("    3. Argon2d  (Data-dependent - maximum resistance against GPU attacks)")
    var_choice = input("  Variant [1/2/3, default 1]: ").strip()

    variant_map = {"1": Type.ID, "2": Type.I, "3": Type.D}
    variant_name = {"1": "Argon2id", "2": "Argon2i", "3": "Argon2d"}
    chosen_type = variant_map.get(var_choice, Type.ID)
    chosen_name = variant_name.get(var_choice, "Argon2id")

    mem_input = input("  Memory cost in KiB (default 65536 = 64MB): ").strip()
    time_input = input("  Time cost (iterations) (default 3): ").strip()
    par_input = input("  Parallelism (threads) (default 4): ").strip()

    mem_cost = int(mem_input) if mem_input.isdigit() and int(mem_input) > 0 else 65536
    time_cost = int(time_input) if time_input.isdigit() and int(time_input) > 0 else 3
    parallelism = int(par_input) if par_input.isdigit() and int(par_input) > 0 else 4

    ph = PasswordHasher(
        time_cost=time_cost,
        memory_cost=mem_cost,
        parallelism=parallelism,
        hash_len=32,
        salt_len=16,
        type=chosen_type
    )

    print(f"\n  Hashing with {chosen_name} (m={mem_cost} KiB, t={time_cost}, p={parallelism})...")
    t0 = time.perf_counter()
    hashed_str = ph.hash(password)
    ms = (time.perf_counter() - t0) * 1000

    print(f"\n  [Success] Hashed in {ms:.2f} ms")
    print(f"  Encoded Argon2 Hash: {hashed_str}")

    save = input("\n  Save hash output? (y/n): ").strip().lower()
    if save == "y":
        out = (
            f"Argon2 Password Hash Output\n"
            f"---------------------------\n"
            f"Variant     : {chosen_name}\n"
            f"Memory Cost : {mem_cost} KiB\n"
            f"Time Cost   : {time_cost}\n"
            f"Parallelism : {parallelism}\n"
            f"Hash String : {hashed_str}\n"
        )
        _save_output(out, "argon2_output.txt")


def verify_password_demo() -> None:
    print("\n--- Argon2 Password Verification ---")
    if not _ARGON2_AVAILABLE:
        print("  [Error] argon2-cffi not installed. Run: pip install argon2-cffi")
        return

    password = input("  Create password to store: ").strip()
    if not password:
        return

    ph = PasswordHasher()
    hashed_str = ph.hash(password)
    print(f"  Stored Hash: {hashed_str[:35]}...")

    attempt = input("\n  Enter password to verify: ").strip()
    t0 = time.perf_counter()
    try:
        ph.verify(hashed_str, attempt)
        ms = (time.perf_counter() - t0) * 1000
        print(f"  ✅ [PASS] Password verified successfully in {ms:.2f} ms!")
        if ph.check_needs_rehash(hashed_str):
            print("  ℹ️ Note: Stored hash parameters differ from current policy; rehash advised.")
    except VerifyMismatchError:
        ms = (time.perf_counter() - t0) * 1000
        print(f"  ❌ [FAIL] Password mismatch! Verified in {ms:.2f} ms.")


def show_how_argon2_works() -> None:
    print("\n--- How Argon2 Works ---")
    print("""
  Argon2 is the winner of the 2015 Password Hashing Competition (PHC) and is
  standardized in RFC 9106. It represents the current gold standard for password hashing.

  The Three Variants:
    1. Argon2d (Data-dependent):
       Memory access locations depend on previous hash values.
       -> Maximizes resistance against GPU/ASIC cracking, but susceptible to
          cache-timing side-channel attacks. Ideal for cryptocurrencies.
    2. Argon2i (Data-independent):
       Memory access locations are computed in advance independently of secret data.
       -> Completely immune to cache-timing attacks, but slightly more vulnerable
          to trade-off attacks. Ideal for password authentication on shared hardware.
    3. Argon2id (Hybrid):
       Begins as Argon2i for the first pass to mitigate side-channel leaks, then
       transitions to Argon2d for subsequent passes to maximize GPU resistance.
       -> Standard recommendation for general web and password authentication!

  Parameters:
    - m (Memory): Memory consumption in KiB (e.g. 65,536 KiB = 64 MB).
    - t (Time): Number of passes over the memory matrix (default 3).
    - p (Parallelism): Number of independent execution lanes/threads (default 4).
    """)


def argon2_menu() -> None:
    while True:
        print("\n--- Argon2 (PHC Winner - RFC 9106) ---")
        print("  Category: Password Hashing & Key Derivation (Level 06)")
        print("  Standard: RFC 9106 / Password Hashing Competition")
        print()
        print("  1. Hash Password with Argon2id / Argon2i / Argon2d")
        print("  2. Verify Password against Argon2 Hash")
        print("  3. How Argon2 Works (Architecture & Variants)")
        print("  4. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            hash_password_demo()
        elif choice == "2":
            verify_password_demo()
        elif choice == "3":
            show_how_argon2_works()
        elif choice == "4":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–4.")

