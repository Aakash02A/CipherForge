import os
import secrets
from cryptography.hazmat.primitives.kdf.hkdf import HKDF, HKDFExpand
from cryptography.hazmat.primitives import hashes


def _save_output(content: str, filename: str = "hkdf_output.txt") -> None:
    os.makedirs("samples", exist_ok=True)
    path = os.path.join("samples", filename)
    try:
        with open(path, "w") as f:
            f.write(content)
        print(f"  [Saved] → {path}")
    except OSError as e:
        print(f"  [Error] Failed to save file: {e}")


def derive_keys_demo() -> None:
    print("\n--- HKDF (Extract-and-Expand) Key Derivation ---")
    ikm_input = input("  Enter Input Keying Material (IKM) or press Enter for random 32 bytes: ").strip()
    if ikm_input:
        ikm = ikm_input.encode("utf-8")
    else:
        ikm = secrets.token_bytes(32)
        print(f"  Generated random IKM (hex): {ikm.hex()}")

    salt_input = input("  Enter Salt (press Enter for random 16 bytes): ").strip()
    salt = salt_input.encode("utf-8") if salt_input else secrets.token_bytes(16)

    info_enc = input("  Context string for Encryption Key [default: 'app-aes-key']: ").strip() or "app-aes-key"
    info_mac = input("  Context string for Authentication Key [default: 'app-mac-key']: ").strip() or "app-mac-key"

    # Derive two independent, domain-separated cryptographic keys from a single master secret
    hkdf_enc = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info_enc.encode("utf-8")
    )
    key_enc = hkdf_enc.derive(ikm)

    hkdf_mac = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=info_mac.encode("utf-8")
    )
    key_mac = hkdf_mac.derive(ikm)

    print("\n  [Success] HKDF-SHA256 Multi-Key Derivation Completed:")
    print(f"  Salt (hex)         : {salt.hex() if isinstance(salt, bytes) else salt}")
    print(f"  Derived Encryption Key (32 bytes) : {key_enc.hex()}")
    print(f"    Info Context     : '{info_enc}'")
    print(f"  Derived MAC Key (32 bytes)        : {key_mac.hex()}")
    print(f"    Info Context     : '{info_mac}'")
    print("\n  Notice: Both keys are derived from the exact same secret, but cryptographically independent!")

    save = input("\n  Save derivation output? (y/n): ").strip().lower()
    if save == "y":
        out = (
            f"HKDF-SHA256 Derivation Output\n"
            f"-----------------------------\n"
            f"IKM (hex)  : {ikm.hex()}\n"
            f"Salt (hex) : {salt.hex() if isinstance(salt, bytes) else salt}\n"
            f"Key 1 ({info_enc}): {key_enc.hex()}\n"
            f"Key 2 ({info_mac}): {key_mac.hex()}\n"
        )
        _save_output(out, "hkdf_output.txt")


def show_how_hkdf_works() -> None:
    print("\n--- How HKDF Works (RFC 5869) ---")
    print("""
  HKDF follows the "Extract-then-Expand" paradigm.

  Stage 1: HKDF-Extract(Salt, IKM) -> PRK
    - Takes non-uniform input keying material (IKM), like a Diffie-Hellman
      shared secret, and concentrates its entropy into a fixed-length
      Pseudorandom Key (PRK) using HMAC:
        PRK = HMAC-Hash(Salt, IKM)

  Stage 2: HKDF-Expand(PRK, info, L) -> OKM
    - Expands the PRK into any desired length of Output Keying Material (OKM)
      using a domain-separation label 'info':
        T(0) = ""
        T(1) = HMAC-Hash(PRK, T(0) || info || 0x01)
        T(2) = HMAC-Hash(PRK, T(1) || info || 0x02)
        ...
        OKM = T(1) || T(2) || ... (truncated to length L)

  Why HKDF is Crucial in Modern Security:
    - TLS 1.3 Key Schedule: Derives client/server traffic secrets and handshake keys.
    - Signal Double Ratchet: Derives message keys from root and chain keys.
    - WireGuard: Derives transport session keys from Noise protocol DH results.
    """)


def hkdf_menu() -> None:
    while True:
        print("\n--- HKDF (HMAC-based Key Derivation Function) ---")
        print("  Category: Password Hashing & Key Derivation (Level 06)")
        print("  Standard: RFC 5869 / TLS 1.3 / Signal Protocol")
        print()
        print("  1. Derive Domain-Separated Cryptographic Keys")
        print("  2. How HKDF Works (Extract-then-Expand)")
        print("  3. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            derive_keys_demo()
        elif choice == "2":
            show_how_hkdf_works()
        elif choice == "3":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–3.")

