import os
import pytest
import importlib

secure_vault = importlib.import_module("level-08-capstone-project.secure_vault")


def test_file_vault_encryption_decryption(tmp_path):
    src_file = tmp_path / "secret.txt"
    vault_file = tmp_path / "secret.vault"
    out_file = tmp_path / "decrypted.txt"

    original_content = b"TOP SECRET: CipherForge Capstone Cryptographic Verification"
    src_file.write_bytes(original_content)

    passphrase = "UltraSecurePassphrase2026!"

    # 1. Encrypt with AES-GCM
    res = secure_vault.encrypt_file_vault(str(src_file), str(vault_file), passphrase, use_chacha=False)
    assert os.path.exists(vault_file)
    assert res["cipher"] == "AES-256-GCM"

    # 2. Decrypt & Verify
    dec_res = secure_vault.decrypt_file_vault(str(vault_file), str(out_file), passphrase)
    assert dec_res["cipher"] == "AES-256-GCM"
    assert out_file.read_bytes() == original_content

    # 3. Wrong passphrase fails
    with pytest.raises(ValueError, match="Decryption failed"):
        secure_vault.decrypt_file_vault(str(vault_file), str(tmp_path / "fail.txt"), "WrongPassphrase")


def test_file_vault_tamper_detection(tmp_path):
    src_file = tmp_path / "doc.txt"
    vault_file = tmp_path / "doc.vault"

    src_file.write_bytes(b"Authorized payment of $50,000")
    passphrase = "VaultKey12345"

    secure_vault.encrypt_file_vault(str(src_file), str(vault_file), passphrase, use_chacha=True)

    # Flip a single bit in the ciphertext payload
    vault_bytes = bytearray(vault_file.read_bytes())
    vault_bytes[-1] ^= 0x01
    tampered_file = tmp_path / "tampered.vault"
    tampered_file.write_bytes(vault_bytes)

    # Tampered vault MUST be detected and rejected by AEAD tag check!
    with pytest.raises(ValueError, match="Decryption failed"):
        secure_vault.decrypt_file_vault(str(tampered_file), str(tmp_path / "tampered_out.txt"), passphrase)


def test_e2ee_messaging_envelope():
    alice = secure_vault.generate_user_identity("Alice")
    bob = secure_vault.generate_user_identity("Bob")

    secret_message = "Hello Bob, this is an authenticated E2EE message from Alice."

    # Alice seals envelope for Bob
    envelope = secure_vault.seal_secure_envelope(alice, bob["dh_pub"], secret_message)

    # Bob opens envelope
    decrypted, sig_valid = secure_vault.open_secure_envelope(bob, envelope)
    assert decrypted == secret_message
    assert sig_valid is True

    # Tampered envelope signature fails
    tampered_envelope = dict(envelope)
    tampered_envelope["ciphertext"] = envelope["ciphertext"][:-4] + "AAAA"
    with pytest.raises(Exception):
        secure_vault.open_secure_envelope(bob, tampered_envelope)

