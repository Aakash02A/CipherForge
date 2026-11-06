import hmac
import hashlib
import blake3


def test_sha256_and_sha3():
    data = b"The quick brown fox jumps over the lazy dog"
    sha256_hex = hashlib.sha256(data).hexdigest()
    sha3_256_hex = hashlib.sha3_256(data).hexdigest()

    assert sha256_hex == "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592"
    assert len(sha3_256_hex) == 64
    assert sha256_hex != sha3_256_hex


def test_blake3():
    data = b"Cryptographic tree hashing"
    hasher = blake3.blake3(data)
    digest = hasher.hexdigest()
    assert len(digest) == 64


def test_hmac_sha256():
    key = b"secret-authentication-key"
    message = b"Authenticate this transaction"

    mac = hmac.new(key, message, hashlib.sha256).hexdigest()
    assert len(mac) == 64

    # Verify matching MAC
    mac2 = hmac.new(key, message, hashlib.sha256).hexdigest()
    assert hmac.compare_digest(mac, mac2)

    # Tampered message must fail
    tampered_mac = hmac.new(key, b"Tampered transaction", hashlib.sha256).hexdigest()
    assert not hmac.compare_digest(mac, tampered_mac)
