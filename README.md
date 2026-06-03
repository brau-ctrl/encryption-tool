<img width="1249" height="425" alt="Screenshot 2026-06-03 140052" src="https://github.com/user-attachments/assets/01592587-fd7f-447d-9248-823d1cf6907a" />
<img width="809" height="371" alt="Screenshot 2026-06-03 140107" src="https://github.com/user-attachments/assets/2b3bf840-3e0d-4488-8592-9c9136e916a8" />


## How encryption_tool.py works

### 1. Cipher engine
- `_shift_char(char, shift)`
  - Shifts one letter by `shift` positions in the alphabet.
  - Keeps uppercase and lowercase separate.
  - Leaves non-letter characters unchanged (`space`, digits, punctuation).

### 2. Caesar cipher
- `caesar_encrypt(plaintext, shift)`
  - Normalizes `shift` with `% 26`.
  - Applies `_shift_char` to every character.
- `caesar_decrypt(ciphertext, shift)`
  - Uses negative shift to reverse encryption.

### 3. Vigenère cipher
- `_clean_key(key)`
  - Removes non-letter characters from the key and uppercases it.
- `vigenere_encrypt(plaintext, key)`
  - Uses a repeating key.
  - Each plaintext letter is shifted by a different key letter.
  - Non-letter plaintext characters do not advance the key position.
- `vigenere_decrypt(ciphertext, key)`
  - Reverses the Vigenère shifts using the same key.

### 4. Display helpers
- `display_result(...)`
  - Prints a formatted result block showing:
    - cipher type
    - key
    - plaintext
    - encrypted text
    - decrypted text
    - verification status

### 5. Interactive CLI
- `main()`
  - Presents a simple command-line menu.
  - Lets the user choose:
    - `1` for Caesar cipher
    - `2` for Vigenère cipher
  - Accepts plaintext input.
  - For Caesar, asks for a numeric shift 1–25.
  - For Vigenère, asks for a keyword.
  - Encrypts, decrypts, and displays the round-trip result.
  - Repeats until user quits.

---

## How test_encryption_tool.py works

- Uses Python `unittest`.
- Tests Caesar cipher behavior:
  - basic shift
  - wrap-around from `Z` to `A`
  - preserving lowercase and punctuation
  - shift normalization (e.g. `29 == 3`)
  - round-trip decrypt(encrypt(x)) == x
- Tests Vigenère cipher behavior:
  - known encryption example
  - round-trip recovery
  - key cycling across plaintext
  - skipping spaces when advancing key
  - invalid key handling
  - case-insensitive keys

---

## Overall behavior

This folder implements a small encryption demo:
- two classical ciphers,
- a CLI user flow,
- and verification via unit tests.

encryption_tool.py is the working program.
test_encryption_tool.py confirms the logic is correct.
