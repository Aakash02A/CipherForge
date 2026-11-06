import os
import sys
import json
import base64
import secrets
import hashlib
import time

from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature, InvalidTag


# ── File & Format Utilities ───────────────────────────────────────────────────

MAGIC_VAULT_HEADER = b"CFVAULT1"  # CipherForge Vault v1 magic bytes
SAMPLES_DIR = "samples"


def _ensure_samples_dir() -> str:
    os.makedirs(SAMPLES_DIR, exist_ok=True)
    return SAMPLES_DIR


def _derive_symmetric_key(passphrase: str, salt: bytes, iterations: int = 300000) -> bytes:
    """Derives a 256-bit symmetric encryption key using PBKDF2-HMAC-SHA256."""
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, iterations, dklen=32)


# ── File Vault Operations ─────────────────────────────────────────────────────

def encrypt_file_vault(source_path: str, dest_path: str, passphrase: str, use_chacha: bool = False) -> dict:
    """
    Encrypts a file with authenticated encryption (AES-256-GCM or ChaCha20-Poly1305).
    Header format: MAGIC (8B) | CIPHER_ID (1B: 1=AES-GCM, 2=ChaCha20) | SALT (16B) | NONCE (12B) | CIPHERTEXT + TAG
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")

    with open(source_path, "rb") as f:
        plaintext = f.read()

    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = _derive_symmetric_key(passphrase, salt)

    cipher_id = b"\x02" if use_chacha else b"\x01"
    cipher_name = "ChaCha20-Poly1305" if use_chacha else "AES-256-GCM"

    # Authenticated Associated Data (binds header to ciphertext)
    aad = MAGIC_VAULT_HEADER + cipher_id + salt + nonce

    t0 = time.perf_counter()
    if use_chacha:
        cipher = ChaCha20Poly1305(key)
        ciphertext = cipher.encrypt(nonce, plaintext, aad)
    else:
        cipher = AESGCM(key)
        ciphertext = cipher.encrypt(nonce, plaintext, aad)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    vault_data = aad + ciphertext

    with open(dest_path, "wb") as f:
        f.write(vault_data)

    sha256_digest = hashlib.sha256(plaintext).hexdigest()
    return {
        "source": source_path,
        "destination": dest_path,
        "cipher": cipher_name,
        "original_size": len(plaintext),
        "encrypted_size": len(vault_data),
        "salt_hex": salt.hex(),
        "nonce_hex": nonce.hex(),
        "sha256_plaintext": sha256_digest,
        "elapsed_ms": elapsed_ms
    }


def decrypt_file_vault(vault_path: str, dest_path: str, passphrase: str) -> dict:
    """
    Decrypts and verifies an authenticated vault file.
    Throws ValueError / InvalidTag if tampering or bad passphrase is detected.
    """
    if not os.path.exists(vault_path):
        raise FileNotFoundError(f"Vault file not found: {vault_path}")

    with open(vault_path, "rb") as f:
        raw = f.read()

    header_len = 8 + 1 + 16 + 12
    if len(raw) < header_len + 16:
        raise ValueError("Corrupted vault file: incomplete header or payload.")

    magic = raw[:8]
    if magic != MAGIC_VAULT_HEADER:
        raise ValueError("Invalid file format: Not a CipherForge vault file.")

    cipher_id = raw[8:9]
    salt = raw[9:25]
    nonce = raw[25:37]
    ciphertext = raw[37:]
    aad = raw[:header_len]

    key = _derive_symmetric_key(passphrase, salt)
    use_chacha = (cipher_id == b"\x02")
    cipher_name = "ChaCha20-Poly1305" if use_chacha else "AES-256-GCM"

    t0 = time.perf_counter()
    try:
        if use_chacha:
            cipher = ChaCha20Poly1305(key)
            plaintext = cipher.decrypt(nonce, ciphertext, aad)
        else:
            cipher = AESGCM(key)
            plaintext = cipher.decrypt(nonce, ciphertext, aad)
    except InvalidTag:
        raise ValueError("Decryption failed: Incorrect passphrase or file tampering detected!")
    elapsed_ms = (time.perf_counter() - t0) * 1000

    with open(dest_path, "wb") as f:
        f.write(plaintext)

    sha256_digest = hashlib.sha256(plaintext).hexdigest()
    return {
        "vault_path": vault_path,
        "destination": dest_path,
        "cipher": cipher_name,
        "decrypted_size": len(plaintext),
        "sha256_plaintext": sha256_digest,
        "elapsed_ms": elapsed_ms
    }


# ── Asymmetric End-to-End Secure Messaging Envelope ───────────────────────────

def generate_user_identity(user_name: str) -> dict:
    """Generates an X25519 encryption keypair and an Ed25519 signing keypair."""
    dh_priv = x25519.X25519PrivateKey.generate()
    dh_pub = dh_priv.public_key()

    sign_priv = ed25519.Ed25519PrivateKey.generate()
    sign_pub = sign_priv.public_key()

    return {
        "user": user_name,
        "dh_priv": dh_priv,
        "dh_pub": dh_pub,
        "sign_priv": sign_priv,
        "sign_pub": sign_pub,
        "dh_pub_bytes": dh_pub.public_bytes_raw(),
        "sign_pub_bytes": sign_pub.public_bytes_raw()
    }


def seal_secure_envelope(
    sender_identity: dict,
    recipient_dh_pub: x25519.X25519PublicKey,
    message: str
) -> dict:
    """
    Creates an authenticated, end-to-end encrypted message envelope:
    1. Ephemeral X25519 key exchange to establish forward secrecy.
    2. HKDF-SHA256 to derive a 256-bit symmetric session key.
    3. ChaCha20-Poly1305 AEAD message encryption.
    4. Ed25519 digital signature over ephemeral pubkey + ciphertext + nonce.
    """
    ephemeral_priv = x25519.X25519PrivateKey.generate()
    ephemeral_pub = ephemeral_priv.public_key()

    # ECDH shared secret
    shared_secret = ephemeral_priv.exchange(recipient_dh_pub)

    # Derive session key via HKDF
    salt = secrets.token_bytes(16)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"CipherForge-Capstone-E2EE-v1"
    )
    session_key = hkdf.derive(shared_secret)

    # AEAD Encryption
    nonce = secrets.token_bytes(12)
    cipher = ChaCha20Poly1305(session_key)
    ciphertext = cipher.encrypt(nonce, message.encode("utf-8"), None)

    # Digital Signature over transcript: Ephemeral Pub || Salt || Nonce || Ciphertext
    transcript = (
        ephemeral_pub.public_bytes_raw() +
        salt +
        nonce +
        ciphertext
    )
    signature = sender_identity["sign_priv"].sign(transcript)

    envelope = {
        "version": 1,
        "sender": sender_identity["user"],
        "sender_sign_pub": base64.b64encode(sender_identity["sign_pub_bytes"]).decode(),
        "ephemeral_dh_pub": base64.b64encode(ephemeral_pub.public_bytes_raw()).decode(),
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "signature": base64.b64encode(signature).decode()
    }
    return envelope


def open_secure_envelope(
    recipient_identity: dict,
    envelope: dict
) -> tuple[str, bool]:
    """
    Verifies sender signature, performs ECDH key agreement, and decrypts message.
    Returns (decrypted_plaintext, is_signature_valid).
    """
    sender_sign_pub_bytes = base64.b64decode(envelope["sender_sign_pub"])
    ephemeral_dh_pub_bytes = base64.b64decode(envelope["ephemeral_dh_pub"])
    salt = base64.b64decode(envelope["salt"])
    nonce = base64.b64decode(envelope["nonce"])
    ciphertext = base64.b64decode(envelope["ciphertext"])
    signature = base64.b64decode(envelope["signature"])

    # 1. Verify Sender's Digital Signature
    transcript = ephemeral_dh_pub_bytes + salt + nonce + ciphertext
    sender_sign_pub = ed25519.Ed25519PublicKey.from_public_bytes(sender_sign_pub_bytes)
    try:
        sender_sign_pub.verify(signature, transcript)
        sig_valid = True
    except InvalidSignature:
        raise ValueError("Cryptographic verification failed: Sender signature is INVALID!")

    # 2. Recompute ECDH Shared Secret
    ephemeral_dh_pub = x25519.X25519PublicKey.from_public_bytes(ephemeral_dh_pub_bytes)
    shared_secret = recipient_identity["dh_priv"].exchange(ephemeral_dh_pub)

    # 3. Derive Session Key via HKDF
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"CipherForge-Capstone-E2EE-v1"
    )
    session_key = hkdf.derive(shared_secret)

    # 4. Decrypt via ChaCha20-Poly1305
    cipher = ChaCha20Poly1305(session_key)
    plaintext_bytes = cipher.decrypt(nonce, ciphertext, None)
    return plaintext_bytes.decode("utf-8"), sig_valid


# ── Interactive CLI Menu ──────────────────────────────────────────────────────

def _ui_encrypt_file() -> None:
    print("\n--- Encrypt File into Secure Vault ---")
    src = input("  Source file path: ").strip()
    if not os.path.exists(src):
        print(f"  [Error] File not found: {src}")
        return

    dst = input("  Destination vault path (e.g. secure.vault): ").strip()
    if not dst:
        dst = src + ".vault"

    passphrase = input("  Enter encryption passphrase: ").strip()
    if not passphrase:
        print("  [Error] Passphrase cannot be empty.")
        return

    algo_choice = input("  Cipher [1=AES-256-GCM (default), 2=ChaCha20-Poly1305]: ").strip()
    use_chacha = (algo_choice == "2")

    try:
        res = encrypt_file_vault(src, dst, passphrase, use_chacha)
        print("\n  🔒 [Success] Vault File Created!")
        print(f"  Cipher        : {res['cipher']}")
        print(f"  Source Size   : {res['original_size']} bytes")
        print(f"  Vault Size    : {res['encrypted_size']} bytes")
        print(f"  Time Taken    : {res['elapsed_ms']:.2f} ms")
        print(f"  Plaintext SHA : {res['sha256_plaintext']}")
    except Exception as e:
        print(f"  [Error] Vault encryption failed: {e}")


def _ui_decrypt_file() -> None:
    print("\n--- Decrypt & Verify Secure Vault ---")
    src = input("  Vault file path: ").strip()
    if not os.path.exists(src):
        print(f"  [Error] File not found: {src}")
        return

    dst = input("  Destination output path: ").strip()
    if not dst:
        dst = "decrypted_output.txt"

    passphrase = input("  Enter decryption passphrase: ").strip()
    try:
        res = decrypt_file_vault(src, dst, passphrase)
        print("\n  🔓 [Success] Vault Decrypted & Authenticated!")
        print(f"  Cipher        : {res['cipher']}")
        print(f"  Output Size   : {res['decrypted_size']} bytes")
        print(f"  Time Taken    : {res['elapsed_ms']:.2f} ms")
        print(f"  Plaintext SHA : {res['sha256_plaintext']}")
        print(f"  Written to    : {dst}")
    except ValueError as ve:
        print(f"\n  ❌ [SECURITY ALERT] {ve}")
    except Exception as e:
        print(f"  [Error] Decryption failed: {e}")


def _ui_messaging_simulation() -> None:
    print("\n--- End-to-End Encrypted Messaging (E2EE) Simulation ---")
    print("  Creating cryptographic identities for Alice and Bob...")

    alice = generate_user_identity("Alice")
    bob = generate_user_identity("Bob")

    print(f"  Alice Ed25519 Identity Key : {alice['sign_pub_bytes'].hex()[:32]}...")
    print(f"  Bob   Ed25519 Identity Key : {bob['sign_pub_bytes'].hex()[:32]}...")

    msg = input("\n  Enter message from Alice to Bob: ").strip() or "Classified Cryptographic Payload: Protocol Omega"
    print("\n  [1] Alice creates sealed envelope (ECDH + HKDF + ChaCha20-Poly1305 + Ed25519 Signature)...")
    envelope = seal_secure_envelope(alice, bob["dh_pub"], msg)

    print("\n  Envelope Transcript Details:")
    print(f"    - Sender       : {envelope['sender']}")
    print(f"    - Ephemeral DH : {envelope['ephemeral_dh_pub'][:24]}...")
    print(f"    - Ciphertext   : {envelope['ciphertext'][:32]}...")
    print(f"    - Signature    : {envelope['signature'][:32]}...")

    print("\n  [2] Bob receives envelope, verifies Alice's signature, and decrypts...")
    decrypted, valid = open_secure_envelope(bob, envelope)
    print(f"    ✅ Signature Verified : {valid} (Authentic message from Alice)")
    print(f"    🔓 Decrypted Message  : \"{decrypted}\"")


def _ui_tamper_attack_simulation() -> None:
    print("\n--- Cryptographic Tamper & Attack Simulation ---")
    print("  Demonstrating how AEAD authentication tags mathematically detect ciphertext bit-flips.")

    _ensure_samples_dir()
    test_file = os.path.join(SAMPLES_DIR, "tamper_test.txt")
    vault_file = os.path.join(SAMPLES_DIR, "tamper_test.vault")
    restored_file = os.path.join(SAMPLES_DIR, "tamper_restored.txt")

    with open(test_file, "w") as f:
        f.write("CONFIDENTIAL FINANCIAL WIRE: Transfer $100,000 to Account #987654321")

    passphrase = "SecretPassphrase123!"
    encrypt_file_vault(test_file, vault_file, passphrase, use_chacha=False)
    print(f"  1. Encrypted file '{test_file}' into vault '{vault_file}'.")

    # Read vault bytes and flip a single bit inside the ciphertext
    with open(vault_file, "rb") as f:
        vault_bytes = bytearray(f.read())

    # Flip the lowest bit of the last byte in ciphertext
    vault_bytes[-1] ^= 0x01
    tampered_vault = os.path.join(SAMPLES_DIR, "tampered.vault")
    with open(tampered_vault, "wb") as f:
        f.write(vault_bytes)

    print(f"  2. Attacker flipped bit 0 of byte {len(vault_bytes)-1} in the encrypted payload.")
    print("  3. Attempting to decrypt the tampered file...")

    try:
        decrypt_file_vault(tampered_vault, restored_file, passphrase)
        print("  ❌ Vulnerability: Tampered ciphertext was accepted!")
    except ValueError as ve:
        print(f"  🛡️ Protection Confirmed: {ve}")
        print("  The AEAD authentication tag failed verification: Tampering detected and blocked.")


def capstone_menu() -> None:
    while True:
        print("\n╔══════════════════════════════════════════════════════════════════╗")
        print("║   🛡️ Level 08 Capstone: SecureVault & E2EE Messaging CLI         ║")
        print("╚══════════════════════════════════════════════════════════════════╝")
        print("  1. Encrypt File to Authenticated Vault (AES-GCM / ChaCha20)")
        print("  2. Decrypt & Authenticate Vault File")
        print("  3. Run End-to-End Encrypted Messaging (E2EE) Simulation")
        print("  4. Run Tamper Attack & Tag Verification Simulation")
        print("  5. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            _ui_encrypt_file()
        elif choice == "2":
            _ui_decrypt_file()
        elif choice == "3":
            _ui_messaging_simulation()
        elif choice == "4":
            _ui_tamper_attack_simulation()
        elif choice == "5":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–5.")


if __name__ == "__main__":
    capstone_menu()

