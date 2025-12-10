import os
import time
import hashlib
import base64
from cryptography.fernet import Fernet
from PIL import Image

def generate_key(login, password):
    """Створює ключ шифрування Fernet на основі Логіну та Пароля"""
    data = login + password
    digest = hashlib.sha256(data.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_text(text, key):
    """Шифрує текст алгоритмом AES (Fernet)"""
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_text(encrypted_str, key):
    """Розшифровує дані назад у текст"""
    f = Fernet(key)
    return f.decrypt(encrypted_str.encode()).decode()

def text_to_bin(text):
    """Перетворює текст у бінарний рядок"""
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    """Перетворює 8 біт у символ"""
    return chr(int(binary, 2))

def hide_data(image_path, secret_text, output_path):
    """Ховає повідомлення (послідовний запис)"""
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        return False
        
    pixels = img.load()
    width, height = img.size

    secret_text += "||END||"
    binary_msg = text_to_bin(secret_text)
    msg_len = len(binary_msg)

    if msg_len > width * height * 3:
        raise ValueError("Повідомлення занадто велике!")

    data_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if data_index < msg_len:
                r = (r & ~1) | int(binary_msg[data_index])
                data_index += 1
            
            if data_index < msg_len:
                g = (g & ~1) | int(binary_msg[data_index])
                data_index += 1
            
            if data_index < msg_len:
                b = (b & ~1) | int(binary_msg[data_index])
                data_index += 1

            pixels[x, y] = (r, g, b)
            
            if data_index >= msg_len:
                break
        if data_index >= msg_len:
            break
    
    img.save(output_path, 'PNG')
    return True

def extract_data(image_path):
    """Витягує повідомлення (посимвольне зчитування)"""
    try:
        img = Image.open(image_path).convert('RGB')
    except FileNotFoundError:
        return None
        
    pixels = img.load()
    width, height = img.size

    delimiter = "||END||"
    current_bits = ""
    decoded_text = ""
    print(f"[*] Сканування зображення {width}x{height}...")

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            for val in [r, g, b]:
                current_bits += str(val & 1)

                if len(current_bits) >= 8:
                    byte = current_bits[:8]
                    char = bin_to_text(byte)
                    decoded_text += char
                    current_bits = current_bits[8:]

                    if decoded_text.endswith(delimiter):
                        print("[INFO] Мітку знайдено! Зупинка сканування.")
                        return decoded_text[:-len(delimiter)]

    print("[INFO] Сканування завершено. Мітку не знайдено.")
    return None

def print_analytics(metrics):
    print("\n" + "="*40)
    print("      ЗВІТ АНАЛІТИКИ ЗАХИСТУ")
    print("="*40)
    print(f"Час шифрування (AES):      {metrics['enc_time']:.4f} сек")
    print(f"Час стеганографії:         {metrics['stego_time']:.4f} сек")
    print("-" * 40)
    print(f"Розмір оригіналу:          {metrics['orig_size']} байт")
    print(f"Розмір шифротексту:        {metrics['enc_size']} байт")
    print(f"Розмір стегоконтейнера:    {metrics['stego_size']} байт")
    print("="*40 + "\n")

def protect_file():
    print("\n--- РЕЖИМ ЗАХИСТУ ФАЙЛУ ---")
    filename = input("Введіть ім'я файлу з текстом (напр. test.txt): ")
    imgname = input("Введіть ім'я картинки-носія (напр. photo.png): ")
    
    if not os.path.exists(filename) or not os.path.exists(imgname):
        print("ПОМИЛКА: Файли не знайдено.")
        return

    login = input("Введіть Email/Логін (для ключа): ")
    password = input("Введіть Пароль (для ключа): ")
    
    metrics = {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        original_text = f.read()
    metrics['orig_size'] = len(original_text.encode('utf-8'))

    print("\n[Етап 1] Шифрування даних...")
    start_t = time.time()
    key = generate_key(login, password)
    encrypted_msg = encrypt_text(original_text, key)
    metrics['enc_time'] = time.time() - start_t
    metrics['enc_size'] = len(encrypted_msg.encode('utf-8'))

    print("[Етап 2] Стеганографія (приховування)...")
    output_stego = "stego_" + imgname
    start_t = time.time()
    
    try:
        if hide_data(imgname, encrypted_msg, output_stego):
            metrics['stego_time'] = time.time() - start_t
            metrics['stego_size'] = os.path.getsize(output_stego)
            
            print(f"УСПІШНО! Файл збережено як '{output_stego}'")
            print_analytics(metrics)
        else:
            print("ПОМИЛКА при збереженні.")

    except ValueError as e:
        print(f"ПОМИЛКА стеганографії: {e}")
    except Exception as e:
        print(f"Невідома ПОМИЛКА: {e}")

def run_recovery():
    print("\n--- РЕЖИМ ВІДНОВЛЕННЯ ---")
    stego_image = input("Введіть ім'я файлу з секретом (напр. stego_photo.png): ")
    
    if not os.path.exists(stego_image):
        print("ПОМИЛКА: Файл не знайдено.")
        return

    print("Витягую дані з зображення...")
    extracted_data = extract_data(stego_image)
    
    if not extracted_data:
        print("ПОМИЛКА: Нічого не знайдено або файл пошкоджено.")
        return

    print("\nДля розшифрування введіть ключі:")
    login = input("Email: ")
    password = input("Пароль: ")
    
    try:
        key = generate_key(login, password)
        decrypted_text = decrypt_text(extracted_data, key)
        
        output_file = "restored_final.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(decrypted_text)
            
        print(f"УСПІШНО! Файл відновлено: {output_file}")
        print(f"Початок вмісту: {decrypted_text[:50]}...")
        
    except Exception:
        print("ПОМИЛКА: Невірний пароль/логін або дані пошкоджені.")

def main():
    while True:
        print("\n=== КОМПЛЕКСНА СИСТЕМА ЗАХИСТУ ===")
        print("1. Захистити файл (Шифрування + Стеганографія)")
        print("2. Відновити файл (Вилучення + Розшифрування)")
        print("3. Вихід")
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            protect_file()
        elif choice == '2':
            run_recovery()
        elif choice == '3':
            print("Робота завершена.")
            break
        else:
            print("Невірний вибір.")

if __name__ == "__main__":
    main()
