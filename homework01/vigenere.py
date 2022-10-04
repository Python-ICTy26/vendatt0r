def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        lettercode: int = ord(plaintext[i])
        if ord("A") <= ord(keyword[i % len(keyword)]) <= ord("Z"):
            shift = ord(keyword[i % len(keyword)]) - ord("A")
        else:
            shift = ord(keyword[i % len(keyword)]) - ord("a")
        if ord("A") <= lettercode <= ord("Z") - shift:
            ciphertext += chr(lettercode + shift)
        elif ord("Z") - shift + 1 <= lettercode <= ord("Z"):
            ciphertext += chr(lettercode - 26 + shift)
        elif ord("a") <= lettercode <= ord("z") - shift:
            ciphertext += chr(lettercode + shift)
        elif ord("z") - shift + 1 <= lettercode <= ord("z"):
            ciphertext += chr(lettercode - 26 + shift)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        lettercode: int = ord(ciphertext[i])
        if ord("A") <= ord(keyword[i % len(keyword)]) <= ord("Z"):
            shift = ord(keyword[i % len(keyword)]) - ord("A")
        else:
            shift = ord(keyword[i % len(keyword)]) - ord("a")
        if ord("A") + shift <= lettercode <= ord("Z"):
            plaintext += chr(lettercode - shift)
        elif ord("A") <= lettercode <= ord("A") + shift - 1:
            plaintext += chr(lettercode + 26 - shift)
        elif ord("a") + shift <= lettercode <= ord("z"):
            plaintext += chr(lettercode - shift)
        elif ord("a") <= lettercode <= ord("a") + shift - 1:
            plaintext += chr(lettercode + 26 - shift)
        else:
            plaintext += ciphertext[i]
    return plaintext
