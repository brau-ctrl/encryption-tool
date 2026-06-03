"""
DecodeLabs — Project 2
Unit tests for encryption_tool.py

Run with:  python test_encryption_tool.py
"""

import unittest
from encryption_tool import (
    caesar_encrypt, caesar_decrypt,
    vigenere_encrypt, vigenere_decrypt,
)


class TestCaesarCipher(unittest.TestCase):

    # ── Core shift math ────────────────────────────────────────────────────────
    def test_encrypt_shift3(self):
        # Classic Caesar: A→D, B→E, Z→C
        self.assertEqual(caesar_encrypt("ABC", 3), "DEF")

    def test_wrap_around(self):
        # Y(24) + 3 = 27 % 26 = 1 = B  (matches slide 10 example)
        self.assertEqual(caesar_encrypt("XYZ", 3), "ABC")

    def test_lowercase_preserved(self):
        self.assertEqual(caesar_encrypt("abc", 3), "def")

    def test_mixed_case(self):
        self.assertEqual(caesar_encrypt("Hello", 3), "Khoor")

    # ── Edge cases ─────────────────────────────────────────────────────────────
    def test_spaces_unchanged(self):
        result = caesar_encrypt("Hello World", 3)
        self.assertIn(" ", result)

    def test_digits_unchanged(self):
        result = caesar_encrypt("abc123", 5)
        self.assertTrue(result.endswith("123"))

    def test_punctuation_unchanged(self):
        result = caesar_encrypt("Hi!", 3)
        self.assertTrue(result.endswith("!"))

    def test_empty_string(self):
        self.assertEqual(caesar_encrypt("", 5), "")

    # ── Key normalisation ──────────────────────────────────────────────────────
    def test_shift_26_is_identity(self):
        # Shifting by 26 returns the same text
        self.assertEqual(caesar_encrypt("Hello", 26), "Hello")

    def test_shift_29_equals_shift_3(self):
        self.assertEqual(caesar_encrypt("Hello", 29), caesar_encrypt("Hello", 3))

    # ── Round-trip: decrypt(encrypt(x)) == x ──────────────────────────────────
    def test_roundtrip_simple(self):
        original = "DecodeLabs"
        self.assertEqual(caesar_decrypt(caesar_encrypt(original, 7), 7), original)

    def test_roundtrip_full_sentence(self):
        original = "The quick brown fox jumps over the lazy dog."
        for shift in [1, 13, 25]:
            self.assertEqual(
                caesar_decrypt(caesar_encrypt(original, shift), shift),
                original,
                msg=f"Round-trip failed for shift={shift}"
            )

    def test_known_ciphertext(self):
        # "KHOOR" is the classic Caesar-3 encryption of "HELLO"
        self.assertEqual(caesar_decrypt("KHOOR", 3), "HELLO")


class TestVigenereCipher(unittest.TestCase):

    def test_encrypt_basic(self):
        # "HELLO" with key "KEY" → known result
        self.assertEqual(vigenere_encrypt("HELLO", "KEY"), "RIJVS")

    def test_roundtrip(self):
        original = "Attack at dawn"
        key = "LEMON"
        self.assertEqual(
            vigenere_decrypt(vigenere_encrypt(original, key), key),
            original
        )

    def test_key_cycles(self):
        # Key shorter than plaintext — must cycle
        original = "ABCDEFGHIJ"
        key = "AB"
        encrypted = vigenere_encrypt(original, key)
        self.assertEqual(vigenere_decrypt(encrypted, key), original)

    def test_spaces_skipped_in_key_cycling(self):
        # Spaces don't consume a key character
        original = "Hello World"
        key = "KEY"
        encrypted = vigenere_encrypt(original, key)
        self.assertEqual(vigenere_decrypt(encrypted, key), original)

    def test_invalid_key_raises(self):
        with self.assertRaises(ValueError):
            vigenere_encrypt("Hello", "123")

    def test_case_insensitive_key(self):
        # "key" and "KEY" should produce identical results
        self.assertEqual(
            vigenere_encrypt("Hello", "key"),
            vigenere_encrypt("Hello", "KEY")
        )


if __name__ == "__main__":
    print("Running DecodeLabs Project 2 — Test Suite\n")
    unittest.main(verbosity=2)
