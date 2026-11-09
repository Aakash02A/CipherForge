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

def test_caesar_auto_solve_no_english_letters():
    caesar = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.Caesar")
    assert caesar.auto_solve_caesar("") == []
    assert caesar.auto_solve_caesar("12345!@#$%^&*()_+") == []
    assert caesar.auto_solve_caesar("Привет, мир! 🚀 12345") == []
    assert caesar.auto_solve_caesar("日本語のテキスト") == []
    assert caesar.auto_solve_caesar("ß") == []


def test_caesar_unicode_and_special_characters_preservation():
    caesar = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.Caesar")
    plaintext = "DEFEND THE CASTLE AT DAWN! Привет мир! 🚀 12345"
    shift = 7
    ciphertext = caesar._caesar_process(plaintext, shift, decrypt=False)
    assert "Привет мир! 🚀 12345" in ciphertext
    decrypted = caesar._caesar_process(ciphertext, shift, decrypt=True)
    assert decrypted == plaintext

    candidates = caesar.auto_solve_caesar(ciphertext)
    assert len(candidates) == 25
    best_shift, recovered_text, _ = candidates[0]
    assert best_shift == shift
    assert recovered_text == plaintext


def test_caesar_auto_solve_does_not_count_unicode_case_expansions():
    caesar = importlib.import_module("level-01-classical-ciphers.traditional-ciphers.Caesar")
    ciphertext = caesar._caesar_process(
        "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG AND LEARNS CRYPTOGRAPHY",
        9,
    )

    baseline = caesar.auto_solve_caesar(ciphertext)
    with_sharp_s = caesar.auto_solve_caesar(ciphertext + "ß")

    assert [(shift, score) for shift, _, score in with_sharp_s] == [
        (shift, score) for shift, _, score in baseline
    ]
    assert all(plaintext.endswith("ß") for _, plaintext, _ in with_sharp_s)
