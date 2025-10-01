def caesar(text, shift, decrypt=False):
    result = ""
    if decrypt: shift = -shift
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def vigenere(text, key, decrypt=False):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            char = char.upper()
            shift = ord(key[key_index % len(key)]) - 65
            if decrypt: shift = -shift
            encrypted_char = chr((ord(char) - 65 + shift) % 26 + 65)
            result += encrypted_char if is_upper else encrypted_char.lower()
            key_index += 1
        else:
            result += char
    return result

surname = input("Прізвище: ")
caesar_shift = int(input("Зсув для Цезаря: "))
text = input("Введіть текст для шифрування: ")

caesar_key = caesar_shift
vigenere_key = surname

caesar_encrypted = caesar(text, caesar_key)
vigenere_encrypted = vigenere(text, vigenere_key)

caesar_decrypted = caesar(caesar_encrypted, caesar_key, decrypt=True)
vigenere_decrypted = vigenere(vigenere_encrypted, vigenere_key, decrypt=True)

print(f"\n{'='*50}")
print(f"ШИФР ЦЕЗАРЯ (зсув={caesar_key})")
print(f"{'='*50}")
print(f"Зашифровано: {caesar_encrypted}")
print(f"Розшифровано: {caesar_decrypted}")
print(f"Довжина: {len(caesar_encrypted)} символів")

print(f"\n{'='*50}")
print(f"ШИФР ВІЖЕНЕРА (ключ={vigenere_key})")
print(f"{'='*50}")
print(f"Зашифровано: {vigenere_encrypted}")
print(f"Розшифровано: {vigenere_decrypted}")
print(f"Довжина: {len(vigenere_encrypted)} символів")

print(f"\n{'='*50}")
print("ПОРІВНЯЛЬНИЙ АНАЛІЗ")
print(f"{'='*50}")
print(f"{'Параметр':<20} {'Цезар':<25} {'Віженер':<25}")
print(f"{'-'*70}")
print(f"{'Складність ключа':<20} {'Проста (1 число)':<25} {'Середня (слово)':<25}")
print(f"{'Довжина ключа':<20} {'Завжди 1':<25} {f'{len(vigenere_key)} символів':<25}")
print(f"{'Стійкість':<20} {'Низька (26 варіантів)':<25} {'Середня (частотний аналіз)':<25}")
print(f"{'Читабельність':<20} {'Нерозбірливо':<25} {'Повністю втрачається':<25}")

print(f"\nВИСНОВОК: Шифр Віженера надійніший через змінний ключ")

