import os
import sys
import importlib

# ── Console Encoding Guard ────────────────────────────────────────────────────
# The CLI UI relies on box-drawing glyphs and emoji. Force UTF-8 on the standard
# streams so the toolkit never crashes on legacy Windows consoles or when output
# is piped/redirected through a non-UTF-8 code page (Python 3.7+).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# ── CipherForge ───────────────────────────────────────────────────────────────
# Main entry point — connects all registered modules across 8 progressive levels.
# Run: python main.py


# ── Safe Import Helper ────────────────────────────────────────────────────────

def _load(module_path: str, func_name: str):
    """Load a menu function and return the function plus any import error."""
    try:
        module = importlib.import_module(module_path)
        function = getattr(module, func_name, None)
        if function is None:
            return None, AttributeError(f"missing function '{func_name}' in '{module_path}'")
        return function, None
    except Exception as exc:
        return None, exc


def _import(module_path: str, func_name: str):
    """
    Safely import a menu function from a module path.
    Returns the function or None if import fails.
    """
    function, _ = _load(module_path, func_name)
    return function


def _run(module_path: str, func_name: str, label: str) -> None:
    """Import and run a menu function, with graceful error handling."""
    fn = _import(module_path, func_name)
    if fn:
        try:
            fn()
        except KeyboardInterrupt:
            print("\n  [Interrupted] Returning to menu...")
        except Exception as e:
            print(f"\n  [Error] {label} crashed: {e}")
            print(f"  Check that all dependencies are installed.")
            input("  Press Enter to continue...")
    else:
        print(f"\n  [Not Available] {label}")
        print(f"  Module path : {module_path}")
        print(f"  Make sure the file exists and has no import errors.")
        print(f"  Run: python -c \"import importlib; importlib.import_module('{module_path}')\" to debug.")
        input("\n  Press Enter to continue...")


# ── Display Helpers ───────────────────────────────────────────────────────────

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _banner() -> None:
    print("""
╔══════════════════════════════════════════════════════════════════╗
║               🔐  CipherForge Learning Toolkit  🔐                ║
║                                                                  ║
║   Interactive Progressive Mastery from Classical to Post-Quantum ║
║   8 Leveled Modules • 90+ Algorithms • Interactive Capstone Vault║
╚══════════════════════════════════════════════════════════════════╝
    """)


def _header(title: str) -> None:
    width = 66
    print(f"\n{'═' * width}")
    print(f"  {title}")
    print(f"{'═' * width}")


def _sub_header(title: str) -> None:
    print(f"\n  {'─' * 60}")
    print(f"  {title}")
    print(f"  {'─' * 60}")


def _menu_item(num: str, label: str, detail: str = "") -> None:
    if detail:
        print(f"  {num:<6} {label:<38} {detail}")
    else:
        print(f"  {num:<6} {label}")


def _back_option(num: str = "0") -> None:
    print(f"\n  {num}. ← Back to Main Menu")


def _get_choice(prompt: str = "\n  Select option: ") -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "0"


def _show_main_help() -> None:
    print("\n  Command shortcuts:")
    print("    1-8      Open a learning level")
    print("    D        Run diagnostics across all modules")
    print("    S        Setup guide / verify environment")
    print("    H / HELP Show this help")
    print("    CLS      Clear screen and redraw banner")
    print("    Q / QUIT Exit toolkit")


def _resolve_main_choice(choice: str) -> str:
    value = choice.strip().upper()
    aliases = {
        "HELP": "H",
        "H": "H",
        "CLS": "CLS",
        "CLEAR": "CLS",
        "DIAG": "D",
        "DIAGNOSTICS": "D",
        "SETUP": "S",
        "MENU": "M",
        "MAIN": "M",
        "QUIT": "Q",
        "EXIT": "Q",
    }
    return aliases.get(value, value)


def _show_main_menu() -> None:
    _banner()

    print("  Select a Cryptography Learning Level:\n")
    print("  ┌─────────────────────────────────────────────────────────────────┐")
    _menu_item("  1 │", "Level 01: Classical & Historical Ciphers", "6 ciphers")
    _menu_item("  2 │", "Level 02: Symmetric Key Cryptography", "26 algorithms")
    _menu_item("  3 │", "Level 03: Asymmetric / Public Key & DH", "11 schemes")
    _menu_item("  4 │", "Level 04: Cryptographic Hashing, MACs & AEAD", "17 schemes")
    _menu_item("  5 │", "Level 05: Digital Signatures & Protocols", "10 protocols")
    _menu_item("  6 │", "Level 06: Password Hashing & Key Derivation", "5 modern KDFs")
    _menu_item("  7 │", "Level 07: Modern, Advanced & Post-Quantum", "14 schemes")
    _menu_item("  8 │", "Level 08: Capstone Project (SecureVault CLI)", "E2EE & Vault")
    print("  ├─────────────────────────────────────────────────────────────────┤")
    _menu_item("  D │", "Run Diagnostics", f"check all {len(_ALL_MODULES)} modules")
    _menu_item("  S │", "Setup Guide", "dependencies & environment")
    _menu_item("  Q │", "Quit", "exit application")
    print("  └─────────────────────────────────────────────────────────────────┘")

    total = len(_ALL_MODULES)
    print(f"\n  Registered modules: {total}")
    print("  Levels: 8 | Classical: 6 | Symmetric: 26 | Asymmetric: 11 | Hash/MAC/AEAD: 17")
    print("  Signatures/Protocols: 10 | Password/KDF: 5 | Advanced/PQC: 14 | Capstone: 1")
    print("\n  Type 1–8 or a command (D, S, H, CLS, Q).")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 1 — Classical & Historical Ciphers
# ═══════════════════════════════════════════════════════════════════

def menu_classical() -> None:
    base = "level-01-classical-ciphers.traditional-ciphers"
    while True:
        _header("Level 01: Classical & Historical Ciphers")
        print("\n  Pen-and-paper ciphers, substitution, transposition & rotor machines:")
        _menu_item("1", "Caesar Cipher",         "Shift substitution · Brute-force demo")
        _menu_item("2", "Vigenère Cipher",       "Polyalphabetic substitution · Kasiski test")
        _menu_item("3", "Playfair Cipher",       "Digraph substitution · 5x5 key matrix")
        _menu_item("4", "Hill Cipher",           "Matrix linear algebra modulo 26")
        _menu_item("5", "Enigma Machine",        "WWII electro-mechanical rotor simulation")
        _menu_item("6", "Rail Fence Cipher",     "Zigzag transposition · Depth analysis")
        _back_option()

        c = _get_choice()
        if c == "1":
            _run(f"{base}.Caesar", "caesar_menu", "Caesar Cipher")
        elif c == "2":
            _run(f"{base}.Vigenere", "vigenere_menu", "Vigenère Cipher")
        elif c == "3":
            _run(f"{base}.Playfair", "playfair_menu", "Playfair Cipher")
        elif c == "4":
            _run(f"{base}.Hill", "hill_menu", "Hill Cipher")
        elif c == "5":
            _run(f"{base}.Enigma", "enigma_menu", "Enigma Machine")
        elif c == "6":
            _run(f"{base}.rail_fence", "rail_fence_menu", "Rail Fence Cipher")
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 2 — Symmetric Key Cryptography
# ═══════════════════════════════════════════════════════════════════

def menu_symmetric() -> None:
    bc = "level-02-symmetric-crypto.block-ciphers"
    bm = "level-02-symmetric-crypto.cipher-modes"
    sc = "level-02-symmetric-crypto.stream-ciphers"

    while True:
        _header("Level 02: Symmetric Key Cryptography")
        print()
        _sub_header("2.1  Block Ciphers")
        _menu_item("1",  "AES",                    "GCM / CBC · 128/192/256-bit")
        _menu_item("2",  "DES",                    "CBC · 56-bit ⚠ deprecated")
        _menu_item("3",  "3DES (Triple DES)",       "CBC · 168-bit ⚠ deprecated")
        _menu_item("4",  "Blowfish",               "CBC · 128-bit Feistel network")
        _menu_item("5",  "Twofish",                "CBC · 256-bit AES finalist")
        _menu_item("6",  "IDEA",                   "CBC · 128-bit PGP legacy")
        _menu_item("7",  "Camellia",               "CBC · 256-bit NTT / ISO standard")
        _menu_item("8",  "Serpent",                "CBC · 256-bit AES runner-up")
        _menu_item("9",  "RC5",                    "CBC · Variable word/round cipher")
        _menu_item("10", "RC6",                    "CBC · AES finalist with integer multiplication")
        _menu_item("11", "Magma",                  "CBC · GOST R 34.12-2015 64-bit")
        _menu_item("12", "Kuznyechik",             "CBC · GOST R 34.12-2015 128-bit")
        _sub_header("2.2  Block Cipher Modes")
        _menu_item("13", "ECB",                    "Electronic Codebook ⚠ insecure")
        _menu_item("14", "CBC",                    "Cipher Block Chaining")
        _menu_item("15", "CFB",                    "Cipher Feedback")
        _menu_item("16", "OFB",                    "Output Feedback")
        _menu_item("17", "CTR",                    "Counter Mode")
        _menu_item("18", "GCM",                    "Galois/Counter Mode (AEAD)")
        _menu_item("19", "CCM",                    "Counter with CBC-MAC (AEAD)")
        _menu_item("20", "XTS",                    "XEX Tweakable Codebook (Disk Encryption)")
        _sub_header("2.3  Stream Ciphers")
        _menu_item("21", "RC4",                    "⚠ broken — educational only")
        _menu_item("22", "Salsa20",                "eSTREAM portfolio")
        _menu_item("23", "ChaCha20",               "RFC 8439 · TLS 1.3 standard")
        _menu_item("24", "HC-128",                 "eSTREAM hardware profile")
        _menu_item("25", "Rabbit",                 "eSTREAM 128-bit high-speed cipher")
        _menu_item("26", "A5/1",                   "GSM cellular encryption ⚠ broken")
        _back_option()

        c = _get_choice()
        c_map = {
            "1": (f"{bc}.aes", "aes_menu", "AES"),
            "2": (f"{bc}.des", "des_menu", "DES"),
            "3": (f"{bc}.des3", "des3_menu", "3DES"),
            "4": (f"{bc}.blowfish", "blowfish_menu", "Blowfish"),
            "5": (f"{bc}.twofish", "twofish_menu", "Twofish"),
            "6": (f"{bc}.idea", "idea_menu", "IDEA"),
            "7": (f"{bc}.camellia", "camellia_menu", "Camellia"),
            "8": (f"{bc}.serpent", "serpent_menu", "Serpent"),
            "9": (f"{bc}.rc5", "rc5_menu", "RC5"),
            "10": (f"{bc}.rc6", "rc6_menu", "RC6"),
            "11": (f"{bc}.magma", "magma_menu", "Magma"),
            "12": (f"{bc}.kuznyechik", "kuznyechik_menu", "Kuznyechik"),
            "13": (f"{bm}.Ecb", "ecb_menu", "ECB Mode"),
            "14": (f"{bm}.Cbc", "cbc_menu", "CBC Mode"),
            "15": (f"{bm}.Cfb", "cfb_menu", "CFB Mode"),
            "16": (f"{bm}.Ofb", "ofb_menu", "OFB Mode"),
            "17": (f"{bm}.Ctr", "ctr_menu", "CTR Mode"),
            "18": (f"{bm}.Gcm", "gcm_menu", "GCM Mode"),
            "19": (f"{bm}.Ccm", "ccm_menu", "CCM Mode"),
            "20": (f"{bm}.Xts", "xts_menu", "XTS Mode"),
            "21": (f"{sc}.Rc4", "rc4_menu", "RC4"),
            "22": (f"{sc}.Salsa20", "salsa20_menu", "Salsa20"),
            "23": (f"{sc}.Chacha20", "chacha20_menu", "ChaCha20"),
            "24": (f"{sc}.Hc128", "hc128_menu", "HC-128"),
            "25": (f"{sc}.Rabbit", "rabbit_menu", "Rabbit"),
            "26": (f"{sc}.A51", "a51_menu", "A5/1"),
        }
        if c in c_map:
            mod, fn, lbl = c_map[c]
            _run(mod, fn, lbl)
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 3 — Asymmetric / Public Key & Key Exchange
# ═══════════════════════════════════════════════════════════════════

def menu_asymmetric() -> None:
    pke = "level-03-asymmetric-crypto.public-key-encryption"
    kex = "level-03-asymmetric-crypto.key-exchange"
    ecc = "level-03-asymmetric-crypto.elliptic-curves"

    while True:
        _header("Level 03: Asymmetric Key Cryptography & Key Exchange")
        print()
        _sub_header("3.1  Public Key Encryption")
        _menu_item("1",  "RSA",                    "OAEP padding · Factorization hardness")
        _menu_item("2",  "ElGamal",                "Discrete logarithm hardness")
        _menu_item("3",  "Rabin Cryptosystem",     "Quadratic residues modulo N")
        _menu_item("4",  "Paillier",               "Additive homomorphic public key system")
        _sub_header("3.2  Key Exchange & Agreement")
        _menu_item("5",  "Diffie-Hellman (DH)",    "Modular exponentiation key agreement")
        _menu_item("6",  "ECDH",                   "Elliptic Curve Diffie-Hellman")
        _menu_item("7",  "X25519",                 "Curve25519 Montgomery ladder agreement")
        _menu_item("8",  "MQV",                    "Menezes-Qu-Vanstone authenticated DH")
        _sub_header("3.3  Elliptic Curve Foundations")
        _menu_item("9",  "Curve25519 / Ed25519",   "Twisted Edwards curve operations")
        _menu_item("10", "ECC ECDH",               "Weierstrass curve key exchange")
        _menu_item("11", "ECC ECDSA",              "Elliptic curve point multiplication")
        _back_option()

        c = _get_choice()
        c_map = {
            "1": (f"{pke}.rsa", "rsa_menu", "RSA Encryption"),
            "2": (f"{pke}.ElGamal", "elgamal_menu", "ElGamal"),
            "3": (f"{pke}.Rabin", "rabin_menu", "Rabin"),
            "4": (f"{pke}.Paillier", "paillier_menu", "Paillier"),
            "5": (f"{kex}.DiffieHellman", "dh_menu", "Diffie-Hellman"),
            "6": (f"{kex}.ECDH", "ecdh_menu", "ECDH"),
            "7": (f"{kex}.X25519", "x25519_menu", "X25519"),
            "8": (f"{kex}.MQV", "mqv_menu", "MQV"),
            "9": (f"{ecc}.Ed25519", "ed25519_menu", "Ed25519"),
            "10": (f"{ecc}.ECDH", "ecdh_menu", "ECC ECDH"),
            "11": (f"{ecc}.ECDSA", "ecdsa_menu", "ECC ECDSA"),
        }
        if c in c_map:
            mod, fn, lbl = c_map[c]
            _run(mod, fn, lbl)
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 4 — Cryptographic Hashing, MACs & AEAD
# ═══════════════════════════════════════════════════════════════════

def menu_hash_mac_aead() -> None:
    hf = "level-04-hashing-and-macs.hash-functions"
    mc = "level-04-hashing-and-macs.message-authentication"
    ae = "level-04-hashing-and-macs.authenticated-encryption"

    while True:
        _header("Level 04: Cryptographic Hashing, MACs & AEAD")
        print()
        _sub_header("4.1  Cryptographic Hash Functions")
        _menu_item("1",  "MD5",                    "128-bit ⚠ collision-broken")
        _menu_item("2",  "SHA-1",                  "160-bit ⚠ collision-broken")
        _menu_item("3",  "SHA-2",                  "SHA-224 / 256 / 384 / 512")
        _menu_item("4",  "SHA-3",                  "Keccak sponge construction")
        _menu_item("5",  "BLAKE2",                 "BLAKE2b / BLAKE2s high-speed")
        _menu_item("6",  "BLAKE3",                 "Tree hashing · Multi-threaded")
        _menu_item("7",  "RIPEMD-160",             "Bitcoin legacy address hash")
        _menu_item("8",  "Whirlpool",              "512-bit NESSIE standard")
        _menu_item("9",  "Tiger",                  "192-bit 64-bit optimized hash")
        _sub_header("4.2  Message Authentication Codes (MAC)")
        _menu_item("10", "HMAC",                   "Keyed hash with SHA-256")
        _menu_item("11", "CMAC",                   "NIST SP 800-38B cipher-based MAC")
        _menu_item("12", "GMAC",                   "Galois Message Authentication Code")
        _menu_item("13", "Poly1305",               "One-time authenticator modulo 2^130-5")
        _sub_header("4.3  Authenticated Encryption (AEAD)")
        _menu_item("14", "AES-GCM",                "Galois/Counter Mode AEAD")
        _menu_item("15", "AES-CCM",                "Counter with CBC-MAC AEAD")
        _menu_item("16", "ChaCha20-Poly1305",      "RFC 8439 modern AEAD standard")
        _menu_item("17", "AES-OCB",                "Offset Codebook Mode AEAD")
        _back_option()

        c = _get_choice()
        c_map = {
            "1": (f"{hf}.MD5", "md5_menu", "MD5"),
            "2": (f"{hf}.SHA_1", "sha1_menu", "SHA-1"),
            "3": (f"{hf}.SHA_2", "sha2_menu", "SHA-2"),
            "4": (f"{hf}.SHA_3", "sha3_menu", "SHA-3"),
            "5": (f"{hf}.BLAKE2", "blake2_menu", "BLAKE2"),
            "6": (f"{hf}.BLAKE3", "blake3_menu", "BLAKE3"),
            "7": (f"{hf}.RIPEMD_160", "ripemd160_menu", "RIPEMD-160"),
            "8": (f"{hf}.Whirlpool", "whirlpool_menu", "Whirlpool"),
            "9": (f"{hf}.Tiger", "tiger_menu", "Tiger"),
            "10": (f"{mc}.HMAC", "hmac_menu", "HMAC"),
            "11": (f"{mc}.CMAC", "cmac_menu", "CMAC"),
            "12": (f"{mc}.GMAC", "gmac_menu", "GMAC"),
            "13": (f"{mc}.Poly1305", "poly1305_menu", "Poly1305"),
            "14": (f"{ae}.aesgcm", "aesgcm_menu", "AES-GCM"),
            "15": (f"{ae}.aesccm", "aesccm_menu", "AES-CCM"),
            "16": (f"{ae}.chacha20poly1305", "chacha20poly1305_menu", "ChaCha20-Poly1305"),
            "17": (f"{ae}.ocb", "ocb_menu", "AES-OCB"),
        }
        if c in c_map:
            mod, fn, lbl = c_map[c]
            _run(mod, fn, lbl)
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 5 — Digital Signatures & Protocols
# ═══════════════════════════════════════════════════════════════════

def menu_signatures_protocols() -> None:
    ds = "level-05-signatures-and-protocols.digital-signatures"
    pr = "level-05-signatures-and-protocols.protocols"

    while True:
        _header("Level 05: Digital Signatures & Cryptographic Protocols")
        print()
        _sub_header("5.1  Digital Signatures")
        _menu_item("1",  "RSA Signatures",         "PKCS#1 v1.5 & PSS probabilistic")
        _menu_item("2",  "DSA",                    "Digital Signature Standard (FIPS 186)")
        _menu_item("3",  "ECDSA",                  "Elliptic Curve Digital Signature (SECP256k1)")
        _menu_item("4",  "EdDSA (Ed25519)",        "Edwards-curve Digital Signature (RFC 8032)")
        _menu_item("5",  "Schnorr Signatures",     "Linear signature scheme (BIP-340)")
        _sub_header("5.2  Cryptographic Protocols")
        _menu_item("6",  "TLS 1.3 Handshake",      "Simulated ClientHello, Key Share, Finished")
        _menu_item("7",  "IPsec IKEv2",            "Security Associations & Diffie-Hellman")
        _menu_item("8",  "SSH-2",                  "Key Exchange & Transport Protocol")
        _menu_item("9",  "PGP / OpenPGP",          "Hybrid Encryption (Asymmetric + Symmetric)")
        _menu_item("10", "Kerberos",               "Ticket Granting Service (TGS) authentication")
        _back_option()

        c = _get_choice()
        c_map = {
            "1": (f"{ds}.RSA_Signature", "rsa_signature_menu", "RSA Signature"),
            "2": (f"{ds}.dsa", "dsa_menu", "DSA"),
            "3": (f"{ds}.ECDSA", "ecdsa_menu", "ECDSA"),
            "4": (f"{ds}.EdDSA", "eddsa_menu", "EdDSA"),
            "5": (f"{ds}.Schnorr", "schnorr_menu", "Schnorr Signature"),
            "6": (f"{pr}.tls", "tls_menu", "TLS 1.3"),
            "7": (f"{pr}.ipsec", "ipsec_menu", "IPsec"),
            "8": (f"{pr}.ssh", "ssh_menu", "SSH-2"),
            "9": (f"{pr}.pgp", "pgp_menu", "PGP / OpenPGP"),
            "10": (f"{pr}.kerberos", "kerberos_menu", "Kerberos"),
        }
        if c in c_map:
            mod, fn, lbl = c_map[c]
            _run(mod, fn, lbl)
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 6 — Password Hashing & Key Derivation (KDF)
# ═══════════════════════════════════════════════════════════════════

def menu_password_kdf() -> None:
    kdf = "level-06-password-and-kdf.kdf-algorithms"

    while True:
        _header("Level 06: Password Hashing & Key Derivation")
        print("\n  Defense against brute-force, GPU cracking & rainbow tables:")
        _menu_item("1", "PBKDF2",                 "HMAC-SHA256 · NIST SP 800-132 · OWASP (600k rounds)")
        _menu_item("2", "BCrypt",                 "Eksblowfish adaptive work factor · OpenBSD standard")
        _menu_item("3", "Scrypt",                 "Memory-hard KDF (N, r, p) · ASIC/FPGA resistant")
        _menu_item("4", "Argon2",                 "Argon2id/i/d · Password Hashing Competition winner")
        _menu_item("5", "HKDF",                   "HMAC Extract-and-Expand · TLS 1.3 / Signal key schedule")
        _back_option()

        c = _get_choice()
        c_map = {
            "1": (f"{kdf}.pbkdf2", "pbkdf2_menu", "PBKDF2"),
            "2": (f"{kdf}.bcrypt_module", "bcrypt_menu", "BCrypt"),
            "3": (f"{kdf}.scrypt_module", "scrypt_menu", "Scrypt"),
            "4": (f"{kdf}.argon2_module", "argon2_menu", "Argon2"),
            "5": (f"{kdf}.hkdf_module", "hkdf_menu", "HKDF"),
        }
        if c in c_map:
            mod, fn, lbl = c_map[c]
            _run(mod, fn, lbl)
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 7 — Advanced Cryptography & Post-Quantum (PQC)
# ═══════════════════════════════════════════════════════════════════

def menu_advanced_pqc() -> None:
    pqc_kem = "level-07-advanced-and-pqc.post-quantum-kems"
    pqc_sig = "level-07-advanced-and-pqc.post-quantum-signatures"
    he = "level-07-advanced-and-pqc.homomorphic-encryption"
    ss = "level-07-advanced-and-pqc.secret-sharing"
    mpc = "level-07-advanced-and-pqc.secure-computation"
    zkp = "level-07-advanced-and-pqc.zero-knowledge-proofs"

    while True:
        _header("Level 07: Modern, Advanced & Post-Quantum Cryptography")
        print()
        _sub_header("7.1  Post-Quantum Key Encapsulation (KEMs)")
        _menu_item("1",  "CRYSTALS-Kyber",         "ML-KEM · NIST FIPS 203 standard")
        _menu_item("2",  "NTRU",                   "Lattice-based polynomial ring KEM")
        _menu_item("3",  "Classic McEliece",       "Code-based Niederreiter dual scheme")
        _sub_header("7.2  Post-Quantum Digital Signatures")
        _menu_item("4",  "CRYSTALS-Dilithium",     "ML-DSA · NIST FIPS 204 standard")
        _menu_item("5",  "Falcon",                 "FN-DSA · Fast-Fourier lattice signature")
        _menu_item("6",  "SPHINCS+",               "SLH-DSA · Stateless hash-based signatures")
        _sub_header("7.3  Privacy-Preserving & Advanced Cryptography")
        _menu_item("7",  "Fully Homomorphic (FHE)","BFV / CKKS encrypted arithmetic")
        _menu_item("8",  "Partially Homomorphic",  "Paillier additive encryption")
        _menu_item("9",  "Shamir's Secret Sharing","(k, n) threshold polynomial secret sharing")
        _menu_item("10", "Secure Multi-Party (MPC)","Yao's Garbled Circuits & Beaver triples")
        _menu_item("11", "Oblivious Transfer (OT)","1-out-of-2 OT protocol foundation")
        _menu_item("12", "Interactive ZKP",        "Schnorr zero-knowledge proof of knowledge")
        _menu_item("13", "zk-SNARKs",              "Non-interactive succinct arguments (Groth16)")
        _menu_item("14", "zk-STARKs",              "Transparent Scalable ZK arguments")
        _back_option()

        c = _get_choice()
        c_map = {
            "1": (f"{pqc_kem}.kyber", "kyber_menu", "CRYSTALS-Kyber"),
            "2": (f"{pqc_kem}.ntru", "ntru_menu", "NTRU"),
            "3": (f"{pqc_kem}.mceliece", "mceliece_menu", "Classic McEliece"),
            "4": (f"{pqc_sig}.dilithium", "dilithium_menu", "CRYSTALS-Dilithium"),
            "5": (f"{pqc_sig}.falcon", "falcon_menu", "Falcon"),
            "6": (f"{pqc_sig}.sphincsplus", "sphincsplus_menu", "SPHINCS+"),
            "7": (f"{he}.fhe", "fhe_menu", "FHE"),
            "8": (f"{he}.phe", "phe_menu", "PHE"),
            "9": (f"{ss}.Shamir_s_Secret_Sharing", "shamir_menu", "Shamir Secret Sharing"),
            "10": (f"{mpc}.smpc", "smpc_menu", "SMPC"),
            "11": (f"{mpc}.ot", "ot_menu", "Oblivious Transfer"),
            "12": (f"{zkp}.zkp", "zkp_menu", "Interactive ZKP"),
            "13": (f"{zkp}.zksnark", "zksnark_menu", "zk-SNARK"),
            "14": (f"{zkp}.zkstark", "zkstark_menu", "zk-STARK"),
        }
        if c in c_map:
            mod, fn, lbl = c_map[c]
            _run(mod, fn, lbl)
        elif c == "0":
            break
        else:
            print("  [Error] Invalid option.")


# ═══════════════════════════════════════════════════════════════════
# LEVEL 8 — Capstone Project
# ═══════════════════════════════════════════════════════════════════

def menu_capstone() -> None:
    _run("level-08-capstone-project.secure_vault", "capstone_menu", "SecureVault CLI")


# ═══════════════════════════════════════════════════════════════════
# DIAGNOSTICS & SETUP
# ═══════════════════════════════════════════════════════════════════

_ALL_MODULES = [
    # Level 01: Classical Ciphers
    ("level-01-classical-ciphers.traditional-ciphers.Caesar",       "caesar_menu"),
    ("level-01-classical-ciphers.traditional-ciphers.Vigenere",     "vigenere_menu"),
    ("level-01-classical-ciphers.traditional-ciphers.Playfair",     "playfair_menu"),
    ("level-01-classical-ciphers.traditional-ciphers.Hill",         "hill_menu"),
    ("level-01-classical-ciphers.traditional-ciphers.Enigma",       "enigma_menu"),
    ("level-01-classical-ciphers.traditional-ciphers.rail_fence",   "rail_fence_menu"),

    # Level 02: Symmetric — Block Ciphers
    ("level-02-symmetric-crypto.block-ciphers.aes",                 "aes_menu"),
    ("level-02-symmetric-crypto.block-ciphers.des",                 "des_menu"),
    ("level-02-symmetric-crypto.block-ciphers.des3",                "des3_menu"),
    ("level-02-symmetric-crypto.block-ciphers.blowfish",            "blowfish_menu"),
    ("level-02-symmetric-crypto.block-ciphers.twofish",             "twofish_menu"),
    ("level-02-symmetric-crypto.block-ciphers.idea",                "idea_menu"),
    ("level-02-symmetric-crypto.block-ciphers.camellia",            "camellia_menu"),
    ("level-02-symmetric-crypto.block-ciphers.serpent",             "serpent_menu"),
    ("level-02-symmetric-crypto.block-ciphers.rc5",                 "rc5_menu"),
    ("level-02-symmetric-crypto.block-ciphers.rc6",                 "rc6_menu"),
    ("level-02-symmetric-crypto.block-ciphers.magma",               "magma_menu"),
    ("level-02-symmetric-crypto.block-ciphers.kuznyechik",          "kuznyechik_menu"),

    # Level 02: Symmetric — Block Cipher Modes
    ("level-02-symmetric-crypto.cipher-modes.Ecb",                  "ecb_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Cbc",                  "cbc_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Cfb",                  "cfb_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Ofb",                  "ofb_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Ctr",                  "ctr_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Gcm",                  "gcm_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Ccm",                  "ccm_menu"),
    ("level-02-symmetric-crypto.cipher-modes.Xts",                  "xts_menu"),

    # Level 02: Symmetric — Stream Ciphers
    ("level-02-symmetric-crypto.stream-ciphers.Rc4",                "rc4_menu"),
    ("level-02-symmetric-crypto.stream-ciphers.Salsa20",            "salsa20_menu"),
    ("level-02-symmetric-crypto.stream-ciphers.Chacha20",           "chacha20_menu"),
    ("level-02-symmetric-crypto.stream-ciphers.Hc128",              "hc128_menu"),
    ("level-02-symmetric-crypto.stream-ciphers.Rabbit",             "rabbit_menu"),
    ("level-02-symmetric-crypto.stream-ciphers.A51",                "a51_menu"),

    # Level 03: Asymmetric — Public Key Encryption
    ("level-03-asymmetric-crypto.public-key-encryption.rsa",        "rsa_menu"),
    ("level-03-asymmetric-crypto.public-key-encryption.ElGamal",    "elgamal_menu"),
    ("level-03-asymmetric-crypto.public-key-encryption.Rabin",      "rabin_menu"),
    ("level-03-asymmetric-crypto.public-key-encryption.Paillier",   "paillier_menu"),

    # Level 03: Asymmetric — Key Exchange & Curves
    ("level-03-asymmetric-crypto.key-exchange.DiffieHellman",       "dh_menu"),
    ("level-03-asymmetric-crypto.key-exchange.ECDH",                "ecdh_menu"),
    ("level-03-asymmetric-crypto.key-exchange.X25519",              "x25519_menu"),
    ("level-03-asymmetric-crypto.key-exchange.MQV",                 "mqv_menu"),
    ("level-03-asymmetric-crypto.elliptic-curves.Ed25519",          "ed25519_menu"),
    ("level-03-asymmetric-crypto.elliptic-curves.ECDH",             "ecdh_menu"),
    ("level-03-asymmetric-crypto.elliptic-curves.ECDSA",            "ecdsa_menu"),

    # Level 04: Hash Functions
    ("level-04-hashing-and-macs.hash-functions.MD5",                "md5_menu"),
    ("level-04-hashing-and-macs.hash-functions.SHA_1",              "sha1_menu"),
    ("level-04-hashing-and-macs.hash-functions.SHA_2",              "sha2_menu"),
    ("level-04-hashing-and-macs.hash-functions.SHA_3",              "sha3_menu"),
    ("level-04-hashing-and-macs.hash-functions.BLAKE2",             "blake2_menu"),
    ("level-04-hashing-and-macs.hash-functions.BLAKE3",             "blake3_menu"),
    ("level-04-hashing-and-macs.hash-functions.RIPEMD_160",         "ripemd160_menu"),
    ("level-04-hashing-and-macs.hash-functions.Whirlpool",          "whirlpool_menu"),
    ("level-04-hashing-and-macs.hash-functions.Tiger",              "tiger_menu"),

    # Level 04: Message Authentication Codes (MAC)
    ("level-04-hashing-and-macs.message-authentication.HMAC",       "hmac_menu"),
    ("level-04-hashing-and-macs.message-authentication.CMAC",       "cmac_menu"),
    ("level-04-hashing-and-macs.message-authentication.GMAC",       "gmac_menu"),
    ("level-04-hashing-and-macs.message-authentication.Poly1305",   "poly1305_menu"),

    # Level 04: Authenticated Encryption (AEAD)
    ("level-04-hashing-and-macs.authenticated-encryption.aesgcm",   "aesgcm_menu"),
    ("level-04-hashing-and-macs.authenticated-encryption.aesccm",   "aesccm_menu"),
    ("level-04-hashing-and-macs.authenticated-encryption.chacha20poly1305", "chacha20poly1305_menu"),
    ("level-04-hashing-and-macs.authenticated-encryption.ocb",      "ocb_menu"),

    # Level 05: Digital Signatures
    ("level-05-signatures-and-protocols.digital-signatures.RSA_Signature", "rsa_signature_menu"),
    ("level-05-signatures-and-protocols.digital-signatures.dsa",           "dsa_menu"),
    ("level-05-signatures-and-protocols.digital-signatures.ECDSA",         "ecdsa_menu"),
    ("level-05-signatures-and-protocols.digital-signatures.EdDSA",         "eddsa_menu"),
    ("level-05-signatures-and-protocols.digital-signatures.Schnorr",       "schnorr_menu"),

    # Level 05: Cryptographic Protocols
    ("level-05-signatures-and-protocols.protocols.tls",             "tls_menu"),
    ("level-05-signatures-and-protocols.protocols.ipsec",           "ipsec_menu"),
    ("level-05-signatures-and-protocols.protocols.ssh",             "ssh_menu"),
    ("level-05-signatures-and-protocols.protocols.pgp",             "pgp_menu"),
    ("level-05-signatures-and-protocols.protocols.kerberos",        "kerberos_menu"),

    # Level 06: Password Hashing & Key Derivation (KDF)
    ("level-06-password-and-kdf.kdf-algorithms.pbkdf2",             "pbkdf2_menu"),
    ("level-06-password-and-kdf.kdf-algorithms.bcrypt_module",      "bcrypt_menu"),
    ("level-06-password-and-kdf.kdf-algorithms.scrypt_module",      "scrypt_menu"),
    ("level-06-password-and-kdf.kdf-algorithms.argon2_module",      "argon2_menu"),
    ("level-06-password-and-kdf.kdf-algorithms.hkdf_module",        "hkdf_menu"),

    # Level 07: Post-Quantum Cryptography (PQC)
    ("level-07-advanced-and-pqc.post-quantum-kems.kyber",           "kyber_menu"),
    ("level-07-advanced-and-pqc.post-quantum-kems.ntru",            "ntru_menu"),
    ("level-07-advanced-and-pqc.post-quantum-kems.mceliece",        "mceliece_menu"),
    ("level-07-advanced-and-pqc.post-quantum-signatures.dilithium", "dilithium_menu"),
    ("level-07-advanced-and-pqc.post-quantum-signatures.falcon",    "falcon_menu"),
    ("level-07-advanced-and-pqc.post-quantum-signatures.sphincsplus", "sphincsplus_menu"),

    # Level 07: Modern & Advanced Privacy-Preserving
    ("level-07-advanced-and-pqc.zero-knowledge-proofs.zkp",         "zkp_menu"),
    ("level-07-advanced-and-pqc.zero-knowledge-proofs.zksnark",     "zksnark_menu"),
    ("level-07-advanced-and-pqc.zero-knowledge-proofs.zkstark",     "zkstark_menu"),
    ("level-07-advanced-and-pqc.homomorphic-encryption.fhe",        "fhe_menu"),
    ("level-07-advanced-and-pqc.homomorphic-encryption.phe",        "phe_menu"),
    ("level-07-advanced-and-pqc.secure-computation.smpc",           "smpc_menu"),
    ("level-07-advanced-and-pqc.secure-computation.ot",             "ot_menu"),
    ("level-07-advanced-and-pqc.secret-sharing.Shamir_s_Secret_Sharing", "shamir_menu"),

    # Level 08: Capstone Project
    ("level-08-capstone-project.secure_vault",                      "capstone_menu"),
]


def run_diagnostics(pause: bool = True) -> tuple[int, int]:
    """Check which modules import successfully."""
    _header("Module Diagnostics — Import Status Check")
    print(f"\n  Checking {len(_ALL_MODULES)} registered modules across 8 levels...\n")

    ok_count   = 0
    fail_count = 0
    failures   = []

    for mod_path, func_name in _ALL_MODULES:
        fn, error = _load(mod_path, func_name)
        short = mod_path.split(".")[-1]
        category = mod_path.split(".")[0]
        if fn:
            print(f"  ✅ {short:<30}  {category}")
            ok_count += 1
        else:
            print(f"  ❌ {short:<30}  {type(error).__name__}: {error}")
            fail_count += 1
            failures.append((mod_path, error))

    print(f"\n  {'─'*60}")
    print(f"  Total Registered : {len(_ALL_MODULES)}")
    print(f"  ✅ OK            : {ok_count}")
    print(f"  ❌ Failed        : {fail_count}")

    if failures:
        print(f"\n  Failed modules:")
        for path, err in failures:
            print(f"    • {path} ({type(err).__name__}: {err})")
        print(f"\n  Common fixes:")
        print(f"    1. Check file exists at the expected path")
        print(f"    2. Verify dependencies: pip install -r requirements.txt")

    if pause:
        input("\n  Press Enter to return to menu...")
    return ok_count, fail_count


def show_setup_guide() -> None:
    _header("CipherForge Setup Guide")
    print("""
  1. Python Version Check:
     Python 3.10+ is required (3.11+ recommended).

  2. Install Core Dependencies:
     pip install -r requirements.txt

  3. Optional C-Extensions:
     Algorithms like tiger and whirlpool require a C/C++ compiler.
     All other 90+ algorithms run with pure-Python or pre-compiled wheels!

  4. Run Diagnostics:
     Press 'D' in the main menu to verify all 90 modules.
    """)
    input("  Press Enter to return to menu...")


# ── Interactive Loop ──────────────────────────────────────────────────────────

def main() -> None:
    while True:
        _show_main_menu()
        raw_choice = _get_choice()
        c = _resolve_main_choice(raw_choice)

        if c == "1":
            menu_classical()
        elif c == "2":
            menu_symmetric()
        elif c == "3":
            menu_asymmetric()
        elif c == "4":
            menu_hash_mac_aead()
        elif c == "5":
            menu_signatures_protocols()
        elif c == "6":
            menu_password_kdf()
        elif c == "7":
            menu_advanced_pqc()
        elif c == "8":
            menu_capstone()
        elif c == "D":
            run_diagnostics(pause=True)
        elif c == "S":
            show_setup_guide()
        elif c == "H":
            _show_main_help()
            input("\n  Press Enter to continue...")
        elif c == "CLS":
            _clear()
            continue
        elif c == "M":
            continue
        elif c in ("Q", "EXIT", "QUIT"):
            print("\n  Thank you for learning with CipherForge! 🔐\n")
            break
        else:
            print("  [Error] Invalid choice. Enter 1–8, D, S, H, CLS, or Q.")
            import time
            time.sleep(0.8)


if __name__ == "__main__":
    main()
