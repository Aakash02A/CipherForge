import os
import hashlib
import secrets
import time


def _save_output(content: str, filename: str = "scrypt_output.txt") -> None:
    os.makedirs("samples", exist_ok=True)
    path = os.path.join("samples", filename)
    try:
        with open(path, "w") as f:
            f.write(content)
        print(f"  [Saved] → {path}")
    except OSError as e:
        print(f"  [Error] Failed to save file: {e}")


def derive_key_demo() -> None:
    print("\n--- Scrypt Memory-Hard Key Derivation ---")
    password = input("  Enter password: ").strip()
    if not password:
        print("  [Error] Password cannot be empty.")
        return

    print("  Standard parameters:")
    print("    N: CPU/memory cost parameter (must be power of 2, e.g., 16384, 32768, 65536)")
    print("    r: block size parameter (typically 8)")
    print("    p: parallelization parameter (typically 1)")

    n_input = input("  Enter N (default 16384 - 16MB RAM): ").strip()
    n = int(n_input) if n_input.isdigit() and int(n_input) > 0 else 16384

    r_input = input("  Enter r (default 8): ").strip()
    r = int(r_input) if r_input.isdigit() and int(r_input) > 0 else 8

    p_input = input("  Enter p (default 1): ").strip()
    p = int(p_input) if p_input.isdigit() and int(p_input) > 0 else 1

    salt = secrets.token_bytes(16)
    approx_mem_mb = (128 * r * n) / (1024 * 1024)
    print(f"\n  Estimated memory footprint: {approx_mem_mb:.2f} MB")

    t0 = time.perf_counter()
    derived = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=n,
        r=r,
        p=p,
        dklen=32
    )
    ms = (time.perf_counter() - t0) * 1000

    print(f"\n  [Success] Scrypt key derived in {ms:.2f} ms")
    print(f"  Salt (hex)        : {salt.hex()}")
    print(f"  Parameters        : N={n}, r={r}, p={p}")
    print(f"  Derived Key (hex) : {derived.hex()}")

    save = input("\n  Save derivation output? (y/n): ").strip().lower()
    if save == "y":
        out = (
            f"Scrypt Key Derivation Output\n"
            f"----------------------------\n"
            f"Parameters : N={n}, r={r}, p={p}\n"
            f"Salt (hex) : {salt.hex()}\n"
            f"Key (hex)  : {derived.hex()}\n"
        )
        _save_output(out, "scrypt_output.txt")


def benchmark_memory_costs() -> None:
    print("\n--- Scrypt Memory & CPU Cost Benchmark ---")
    password = b"benchmark-secret-password-123"
    salt = b"benchmark_salt16"
    test_ns = [2048, 4096, 8192, 16384, 32768]

    print(f"  {'N':<8} | {'Memory (MB)':<12} | {'Duration (ms)':<15} | {'Recommended For'}")
    print(f"  {'-'*8}-+-{'-'*12}-+-{'-'*15}-+-{'-'*25}")

    for n in test_ns:
        mem_mb = (128 * 8 * n) / (1024 * 1024)
        t0 = time.perf_counter()
        hashlib.scrypt(password, salt=salt, n=n, r=8, p=1, dklen=32)
        ms = (time.perf_counter() - t0) * 1000

        suitability = "Embedded / Low RAM" if n <= 4096 else ("Interactive Web Login" if n <= 16384 else "Sensitive File Encryption")
        print(f"  {n:<8} | {mem_mb:<12.2f} | {ms:<15.2f} | {suitability}")


def show_how_scrypt_works() -> None:
    print("\n--- How Scrypt Works ---")
    print("""
  Scrypt (RFC 7914) was designed in 2009 by Colin Percival specifically to defeat
  custom hardware (ASIC / FPGA) and GPU attacks on password hashes.

  The ASIC / GPU Threat:
    In PBKDF2 or SHA-256, an attacker can build custom silicon with tens of thousands
    of parallel hashing cores on a single chip because very little RAM is required.

  The Memory-Hard Solution:
    Scrypt forces the computing unit to allocate a large array of pseudorandom data
    in RAM (determined by N and r: Memory = 128 * r * N bytes) and repeatedly read from
    pseudorandom indices (ROMix step).
    - Custom ASICs cannot fit thousands of large memory caches without becoming
      prohibitively expensive and physically massive.
    - Thus, custom hardware offers almost no cost-performance advantage over standard CPUs!

  Parameters:
    - N: CPU/memory cost (must be a power of 2, e.g., 2^14 = 16384).
    - r: Block size (default 8, controlling memory sequential access).
    - p: Parallelization parameter (number of independent threads).
    """)


def scrypt_menu() -> None:
    while True:
        print("\n--- Scrypt (Memory-Hard Key Derivation) ---")
        print("  Category: Password Hashing & Key Derivation (Level 06)")
        print("  Standard: RFC 7914 / IETF")
        print()
        print("  1. Derive Encryption Key with Custom Parameters")
        print("  2. Benchmark Memory & CPU Costs (N Scaling)")
        print("  3. How Scrypt Works (Memory-Hard Defense)")
        print("  4. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            derive_key_demo()
        elif choice == "2":
            benchmark_memory_costs()
        elif choice == "3":
            show_how_scrypt_works()
        elif choice == "4":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–4.")

