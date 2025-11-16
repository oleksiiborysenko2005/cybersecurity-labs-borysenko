import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key_from_data(user_data):
    """Генерація валідного ключа для Fernet на основі рядка (Email+Пароль)"""
    # Хешуємо дані (SHA256), щоб отримати 32 байти
    digest = hashlib.sha256(user_data.encode()).digest()
    # Кодуємо в base64, оскільки Fernet вимагає саме такий формат
    return base64.urlsafe_b64encode(digest)

def main():
    while True:
        print("\n--- Шифрування ---")
        print("1. Згенерувати ключ (на основі Email та пароля)")
        print("2. Зашифрувати повідомлення")
        print("3. Розшифрувати повідомлення")
        print("4. Вихід")
        
        choice = input("\nВаш вибір: ")

        if choice == '1':
            email = input("Введіть Email: ")
            password = input("Введіть ключове слово/пароль: ")
            # Генерація ключа
            key = generate_key_from_data(email + password)
            print(f"\nВАШ КЛЮЧ (збережіть його): {key.decode()}")

        elif choice == '2':
            key_input = input("Вставте ваш Ключ: ")
            message = input("Введіть повідомлення: ")
            try:
                f = Fernet(key_input.encode())
                # Шифрування
                token = f.encrypt(message.encode())
                print(f"\nЗашифровані дані:\n{token.decode()}")
            except Exception:
                print("\n[!] Помилка. Перевірте правильність ключа.")

        elif choice == '3':
            key_input = input("Вставте ваш Ключ: ")
            encrypted_message = input("Вставте зашифрований рядок: ")
            try:
                f = Fernet(key_input.encode())
                # Розшифрування
                decrypted = f.decrypt(encrypted_message.encode())
                print(f"\nРозшифроване повідомлення:\n{decrypted.decode()}")
            except Exception:
                print("\n[!] Помилка. Невірний ключ або пошкоджені дані.")

        elif choice == '4':
            break

if __name__ == "__main__":
    main()
