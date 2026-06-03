"""
╔══════════════════════════════════════════════════════════╗
║        DecodeLabs  |  Cybersecurity Internship 2026      ║
║        Project 2   :  Basic Encryption & Decryption      ║
║        Author      :  Sunday Victor       ║
╚══════════════════════════════════════════════════════════╝

CRYPTOGRAPHIC CONCEPTS IMPLEMENTED (from brief):
  • IPO Model      : Input (plaintext) → Process (shift) → Output (ciphertext)
  • ASCII Logic    : Text → integers via ord() before any math is applied
  • Caesar Cipher  : E_n(x) = (x + n) % 26  |  D_n(x) = (x - n) % 26
  • Modular Wrap   : % 26 keeps characters inside the A-Z / a-z boundary
  • Edge Cases     : Spaces, digits, punctuation are passed through unchanged
"""


# ══════════════════════════════════════════════════════════════════════════════
#  CIPHER ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _shift_char(char: str, shift: int) -> str:
    """
    Core transformation: shift a single alphabetic character by `shift` steps.

    Algorithm (from slide 11):
        1. ord(char)          → convert letter to ASCII integer
        2. subtract base      → normalise to 0-25 range  (A=0 … Z=25)
        3. add shift          → apply the key
        4. % 26               → modular wrap (handles Z→A boundary)
        5. add base back      → return to ASCII range
        6. chr(...)           → convert integer back to character

    Non-alpha characters are returned unchanged (edge-case handling).
    Uppercase and lowercase alphabets are treated as separate ranges.
    """
    if char.isupper():
        base = ord('A')                          # uppercase base: 65
        return chr((ord(char) - base + shift) % 26 + base)
    elif char.islower():
        base = ord('a')                          # lowercase base: 97
        return chr((ord(char) - base + shift) % 26 + base)
    else:
        return char                              # space, digit, symbol → unchanged


# ── Caesar Cipher ─────────────────────────────────────────────────────────────

def caesar_encrypt(plaintext: str, shift: int) -> str:
    """
    Encrypt plaintext using the Caesar cipher with the given shift key.
    E_n(x) = (x + n) % 26
    """
    shift = shift % 26                           # normalise key (e.g. 29 == 3)
    return "".join(_shift_char(ch, shift) for ch in plaintext)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """
    Decrypt ciphertext by reversing the shift.
    D_n(x) = (x - n) % 26  ←→  same as encrypting with (26 - shift)
    """
    shift = shift % 26
    return "".join(_shift_char(ch, -shift) for ch in ciphertext)


# ── Vigenère Cipher (bonus — defeats frequency analysis) ─────────────────────

def _clean_key(key: str) -> str:
    """Strip non-alpha characters from key and uppercase it."""
    return "".join(ch.upper() for ch in key if ch.isalpha())


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt using the Vigenère cipher.
    Each alpha character in plaintext is shifted by a different key letter,
    cycling through the key. Non-alpha characters skip a key position.
    """
    key = _clean_key(key)
    if not key:
        raise ValueError("Key must contain at least one alphabetic character.")

    result = []
    key_index = 0
    for ch in plaintext:
        if ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(_shift_char(ch, shift))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt a Vigenère-encrypted ciphertext using the same key."""
    key = _clean_key(key)
    if not key:
        raise ValueError("Key must contain at least one alphabetic character.")

    result = []
    key_index = 0
    for ch in ciphertext:
        if ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(_shift_char(ch, -shift))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


# ══════════════════════════════════════════════════════════════════════════════
#  DISPLAY HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def display_result(plaintext: str, ciphertext: str, decrypted: str,
                   cipher_name: str, key_display: str) -> None:
    """Pretty-print the full IPO result to the terminal."""
    verified = "✓  VERIFIED" if decrypted == plaintext else "✗  MISMATCH"

    print("\n" + "═" * 58)
    print(f"  CIPHER      : {cipher_name}")
    print(f"  KEY         : {key_display}")
    print("─" * 58)
    print(f"  PLAINTEXT   : {plaintext}")
    print(f"  ENCRYPTED   : {ciphertext}")
    print(f"  DECRYPTED   : {decrypted}")
    print("─" * 58)
    print(f"  INTEGRITY   : {verified}  (decrypt(encrypt(x)) == x)")
    print("═" * 58 + "\n")


# ══════════════════════════════════════════════════════════════════════════════
#  INTERACTIVE CLI
# ══════════════════════════════════════════════════════════════════════════════

def get_int(prompt: str, min_val: int, max_val: int) -> int:
    """Prompt until the user enters a valid integer in [min_val, max_val]."""
    while True:
        try:
            value = int(input(prompt).strip())
            if min_val <= value <= max_val:
                return value
            print(f"  [!] Enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Invalid input — please enter an integer.")


def main() -> None:
    print("\n╔══════════════════════════════════════════════╗")
    print("║  DecodeLabs — Encryption & Decryption Tool   ║")
    print("╚══════════════════════════════════════════════╝\n")
    print("  Ciphers available:")
    print("  [1] Caesar Cipher  (shift key, single integer)")
    print("  [2] Vigenère Cipher (keyword, polyalphabetic)\n")
    print("  Type 'quit' at any prompt to exit.\n")

    while True:
        # ── Choose cipher ──────────────────────────────────────────────────
        choice = input("  Select cipher [1/2]: ").strip()
        if choice.lower() == "quit":
            break
        if choice not in ("1", "2"):
            print("  [!] Enter 1 or 2.\n")
            continue

        # ── Get plaintext ──────────────────────────────────────────────────
        text = input("  Enter text to encrypt: ").strip()
        if text.lower() == "quit":
            break
        if not text:
            print("  [!] No text entered.\n")
            continue

        # ── Encrypt / decrypt ──────────────────────────────────────────────
        if choice == "1":
            shift = get_int("  Enter shift key (1–25): ", 1, 25)
            encrypted = caesar_encrypt(text, shift)
            decrypted = caesar_decrypt(encrypted, shift)
            display_result(text, encrypted, decrypted,
                           "Caesar Cipher", f"shift = {shift}")

        else:
            keyword = input("  Enter keyword (letters only): ").strip()
            if keyword.lower() == "quit":
                break
            try:
                encrypted = vigenere_encrypt(text, keyword)
                decrypted = vigenere_decrypt(encrypted, keyword)
                display_result(text, encrypted, decrypted,
                               "Vigenère Cipher", f'keyword = "{keyword.upper()}"')
            except ValueError as e:
                print(f"  [!] {e}\n")
                continue

        another = input("  Encrypt another message? (y/n): ").strip().lower()
        if another != "y":
            break

    print("\n  Session ended. Data confidentiality maintained. 🔐\n")


if __name__ == "__main__":
    main()
