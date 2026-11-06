import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519, ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


def test_ed25519_signature():
    priv = ed25519.Ed25519PrivateKey.generate()
    pub = priv.public_key()
    message = b"Document to sign with Ed25519"

    signature = priv.sign(message)
    assert len(signature) == 64

    # Valid signature passes
    pub.verify(signature, message)

    # Tampered message fails
    with pytest.raises(InvalidSignature):
        pub.verify(signature, b"Tampered document")


def test_ecdsa_p256_signature():
    priv = ec.generate_private_key(ec.SECP256R1())
    pub = priv.public_key()
    message = b"Document to sign with ECDSA"

    signature = priv.sign(message, ec.ECDSA(hashes.SHA256()))

    # Verify
    pub.verify(signature, message, ec.ECDSA(hashes.SHA256()))

    # Tampered signature fails
    tampered_sig = bytearray(signature)
    tampered_sig[-1] ^= 0x01
    with pytest.raises(InvalidSignature):
        pub.verify(bytes(tampered_sig), message, ec.ECDSA(hashes.SHA256()))

