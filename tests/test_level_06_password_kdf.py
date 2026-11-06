import hashlib
import bcrypt
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


def test_pbkdf2_hmac():
    password = b"MasterPassphrase123"
    salt = b"random_salt_1234"
    iterations = 10000

    dk = hashlib.pbkdf2_hmac("sha256", password, salt, iterations, 32)
    assert len(dk) == 32
    # Deterministic test with same parameters
    dk2 = hashlib.pbkdf2_hmac("sha256", password, salt, iterations, 32)
    assert dk == dk2


def test_bcrypt():
    password = b"secure_user_password"
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password, salt)

    assert bcrypt.checkpw(password, hashed) is True
    assert bcrypt.checkpw(b"wrong_password", hashed) is False


def test_scrypt():
    password = b"memory_hard_secret"
    salt = b"scrypt_salt_5678"
    dk = hashlib.scrypt(password, salt=salt, n=2048, r=8, p=1, dklen=32)
    assert len(dk) == 32


def test_argon2id():
    ph = PasswordHasher(time_cost=2, memory_cost=16384, parallelism=2)
    hashed = ph.hash("my_secret_password")

    assert ph.verify(hashed, "my_secret_password") is True


def test_hkdf_domain_separation():
    ikm = b"shared_diffie_hellman_secret_32b"
    salt = b"hkdf_test_salt16"

    hkdf_enc = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"aes-key")
    key_enc = hkdf_enc.derive(ikm)

    hkdf_mac = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b"mac-key")
    key_mac = hkdf_mac.derive(ikm)

    assert len(key_enc) == 32
    assert len(key_mac) == 32
    # Two keys derived from same IKM must be cryptographically distinct!
    assert key_enc != key_mac

