import importlib
import pytest


def test_caesar_cipher():
    caesar = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.Caesar")
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    shift = 7

    encrypted = caesar._caesar_process(plaintext, shift, decrypt=False)
    assert encrypted != plaintext
    decrypted = caesar._caesar_process(encrypted, shift, decrypt=True)
    assert decrypted == plaintext


def test_rail_fence_cipher():
    rf = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.rail_fence")
    plaintext = "DEFENDTHEEASTWALLOFTHECASTLE"
    rails = 4

    ciphertext = rf.rail_fence_encrypt(plaintext, rails)
    assert ciphertext != plaintext
    assert len(ciphertext) == len(plaintext)

    decrypted = rf.rail_fence_decrypt(ciphertext, rails)
    assert decrypted == plaintext


def test_vigenere_cipher():
    vig = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.Vigenere")
    plaintext = "ATTACKATDAWN"
    keyword = "LEMON"

    encrypted = vig._vigenere_process(plaintext, keyword, decrypt=False)
    assert encrypted != plaintext
    decrypted = vig._vigenere_process(encrypted, keyword, decrypt=True)
    assert decrypted == plaintext

def test_caesar_auto_solve():
    caesar = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.Caesar")
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND LEARNS CRYPTOGRAPHY"
    shift = 9
    ciphertext = caesar._caesar_process(plaintext, shift, decrypt=False)

    candidates = caesar.auto_solve_caesar(ciphertext)
    assert len(candidates) == 25
    best_shift, recovered_text, _ = candidates[0]
    assert best_shift == shift
    assert recovered_text == plaintext

