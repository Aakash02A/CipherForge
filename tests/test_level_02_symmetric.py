import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def test_aes_gcm():
    key = AESGCM.generate_key(bit_length=256)
    nonce = secrets.token_bytes(12)
    plaintext = b"Classified Symmetric Payload"
    aad = b"header-metadata-v1"

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    assert ciphertext != plaintext

    decrypted = aesgcm.decrypt(nonce, ciphertext, aad)
    assert decrypted == plaintext


def test_chacha20_poly1305():
    key = ChaCha20Poly1305.generate_key()
    nonce = secrets.token_bytes(12)
    plaintext = b"Stream authenticated payload"
    aad = b"session-metadata"

    cipher = ChaCha20Poly1305(key)
    ciphertext = cipher.encrypt(nonce, plaintext, aad)
    assert ciphertext != plaintext

    decrypted = cipher.decrypt(nonce, ciphertext, aad)
    assert decrypted == plaintext


def test_aes_cbc_padding():
    key = secrets.token_bytes(32)
    iv = secrets.token_bytes(16)
    plaintext = b"Unpadded arbitrary length string"

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_padded) + unpadder.finalize()

    assert unpadded_data == plaintext

