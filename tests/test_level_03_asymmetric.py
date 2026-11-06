from cryptography.hazmat.primitives.asymmetric import rsa, padding, x25519
from cryptography.hazmat.primitives import hashes


def test_rsa_oaep_encryption():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    message = b"Secret Asymmetric Message"

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    assert ciphertext != message

    decrypted = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    assert decrypted == message


def test_x25519_key_exchange():
    alice_priv = x25519.X25519PrivateKey.generate()
    alice_pub = alice_priv.public_key()

    bob_priv = x25519.X25519PrivateKey.generate()
    bob_pub = bob_priv.public_key()

    alice_shared = alice_priv.exchange(bob_pub)
    bob_shared = bob_priv.exchange(alice_pub)

    assert alice_shared == bob_shared
    assert len(alice_shared) == 32

