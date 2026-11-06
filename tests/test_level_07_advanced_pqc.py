import importlib


def test_shamir_secret_sharing():
    ssss = importlib.import_module("level-07-advanced-and-pqc.secret-sharing.Shamir_s_Secret_Sharing")
    scheme = ssss._ShamirsSecretSharing()
    secret = 123456789
    k = 3
    n = 5

    shares = scheme.split(secret, n=n, k=k)
    assert len(shares) == n

    # Reconstruct from exactly k shares
    reconstructed = scheme.reconstruct(shares[:k])
    assert reconstructed == secret

    # Reconstruct from any other subset of k shares
    reconstructed_other = scheme.reconstruct([shares[0], shares[2], shares[4]])
    assert reconstructed_other == secret


def test_paillier_homomorphic_addition():
    paillier = importlib.import_module("level-07-advanced-and-pqc.homomorphic-encryption.phe")
    pk, sk = paillier._paillier_keygen(bits=128)

    m1 = 45
    m2 = 55
    c1 = paillier._paillier_encrypt(pk, m1)
    c2 = paillier._paillier_encrypt(pk, m2)

    # Homomorphic addition of ciphertexts
    c_sum = paillier._paillier_add(pk, c1, c2)
    decrypted_sum = paillier._paillier_decrypt(sk, c_sum)

    assert decrypted_sum == (m1 + m2)
