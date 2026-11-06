import os


def _save_output(content: str, filename: str = "rail_fence_output.txt") -> None:
    os.makedirs("samples", exist_ok=True)
    path = os.path.join("samples", filename)
    try:
        with open(path, "w") as f:
            f.write(content)
        print(f"  [Saved] → {path}")
    except OSError as e:
        print(f"  [Error] Failed to save file: {e}")


def rail_fence_encrypt(text: str, rails: int) -> str:
    if rails <= 1:
        return text

    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    return "".join("".join(row) for row in fence)


def rail_fence_decrypt(cipher: str, rails: int) -> str:
    if rails <= 1:
        return cipher

    # Mark the zigzag pattern with placeholders
    pattern = [[None] * len(cipher) for _ in range(rails)]
    rail = 0
    direction = 1

    for col in range(len(cipher)):
        pattern[rail][col] = '*'
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    # Fill in the characters along the marked pattern
    idx = 0
    for r in range(rails):
        for c in range(len(cipher)):
            if pattern[r][c] == '*' and idx < len(cipher):
                pattern[r][c] = cipher[idx]
                idx += 1

    # Read off characters in zigzag order
    result = []
    rail = 0
    direction = 1
    for col in range(len(cipher)):
        result.append(pattern[rail][col])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    return "".join(result)


def display_fence_visualization(text: str, rails: int) -> None:
    if rails <= 1 or not text:
        return

    grid = [[" " for _ in range(len(text))] for _ in range(rails)]
    rail = 0
    direction = 1

    for col, char in enumerate(text):
        grid[rail][col] = char
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    print("\n  Zigzag Rail Visualization:")
    for r, row in enumerate(grid):
        print(f"    Rail {r+1}: " + "".join(row))


def encrypt_demo() -> None:
    print("\n--- Rail Fence Cipher Encryption ---")
    text = input("  Enter plaintext: ").strip()
    if not text:
        print("  [Error] Text cannot be empty.")
        return

    rails_str = input("  Enter number of rails [2-10, default 3]: ").strip()
    rails = int(rails_str) if rails_str.isdigit() and int(rails_str) >= 2 else 3

    ciphertext = rail_fence_encrypt(text, rails)
    print(f"\n  Ciphertext: {ciphertext}")
    display_fence_visualization(text, rails)

    save = input("\n  Save output to file? (y/n): ").strip().lower()
    if save == "y":
        _save_output(f"Plaintext : {text}\nRails     : {rails}\nCiphertext: {ciphertext}\n", "rail_fence_output.txt")


def decrypt_demo() -> None:
    print("\n--- Rail Fence Cipher Decryption ---")
    ciphertext = input("  Enter ciphertext: ").strip()
    if not ciphertext:
        print("  [Error] Ciphertext cannot be empty.")
        return

    rails_str = input("  Enter number of rails used [2-10, default 3]: ").strip()
    rails = int(rails_str) if rails_str.isdigit() and int(rails_str) >= 2 else 3

    plaintext = rail_fence_decrypt(ciphertext, rails)
    print(f"\n  Decrypted Plaintext: {plaintext}")
    display_fence_visualization(plaintext, rails)


def show_how_it_works() -> None:
    print("\n--- How the Rail Fence Cipher Works ---")
    print("""
  The Rail Fence Cipher (also called the Zigzag Cipher) is a classic transposition
  cipher where plaintext is written downwards diagonally on successive 'rails' of
  an imaginary fence, then moving upwards when the bottom rail is reached.

  Example with 3 rails and plaintext 'WE ARE DISCOVERED':
    Rail 1: W . . . E . . . C . . . V . . . E . . .
    Rail 2: . E . R . D . S . O . E . R . D . F . .
    Rail 3: . . A . . . I . . . V . . . E . . . . .

  Transposition vs. Substitution:
    Unlike Caesar or Vigenère which substitute characters, Rail Fence rearranges
    the order of letters without altering their identities. Letter frequency
    analysis reveals exact natural language distribution, making transposition
    ciphers easy to identify and break with anagramming or brute forcing rail counts.
    """)


def rail_fence_menu() -> None:
    while True:
        print("\n--- Rail Fence Cipher (Zigzag Transposition) ---")
        print("  Category: Classical & Historical Ciphers (Level 01)")
        print("  Type: Transposition Cipher")
        print()
        print("  1. Encrypt Message")
        print("  2. Decrypt Message")
        print("  3. How Rail Fence Works")
        print("  4. Back")

        choice = input("\n  Select option: ").strip()

        if choice == "1":
            encrypt_demo()
        elif choice == "2":
            decrypt_demo()
        elif choice == "3":
            show_how_it_works()
        elif choice == "4":
            break
        else:
            print("  [Error] Invalid option. Please choose 1–4.")

