
import hashlib
import os

def get_sha256(text: str):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def get_file_content(filename: str):
    """Читає вміст файлу. Повертає (вміст, помилка)"""
    if not os.path.exists(filename):
        return None, f"Помилка: Файл '{filename}' не знайдено."
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read(), None
    except Exception as e:
        return None, f"Помилка читання файлу: {e}"

def generate_keys(personal_data: str):
    private_key = get_sha256(personal_data)
    public_key = get_sha256(private_key)
    return private_key, public_key

def create_signature(document_content: str, private_key: str):
    doc_hash = get_sha256(document_content)
    signature = get_sha256(doc_hash + private_key)
    return signature

def verify_signature(document_content: str, signature: str, private_key: str):
    current_doc_hash = get_sha256(document_content)
    test_signature = get_sha256(current_doc_hash + private_key)
    return test_signature == signature

def main_menu():
    private_key = None
    public_key = None
    signature = None
    signed_doc_name = ""

    while True:
        print("\n--- Меню Системи Цифрового Підпису ---")
        print("1. Згенерувати нову пару ключів")
        print("2. Підписати документ")
        print("3. Перевірити підпис документа")
        print("4. Вийти")
        choice = input("Ваш вибір (1-4): ")

        if choice == '1':
            name = input("Введіть ім'я: ")
            date = input("Введіть дату: ")
            secret = input("Введіть секретне слово: ")
            
            personal_data = name + date + secret
            private_key, public_key = generate_keys(personal_data)
            
            print(f"Ключі згенеровано!")
            print(f"   Публічний ключ (хеш): {public_key}")

        elif choice == '2':
            if not private_key:
                print("\nПомилка: Спочатку згенеруйте ключі (опція 1).")
                continue
                
            signed_doc_name = input("Введіть ім'я файлу для підпису: ")
            content, error = get_file_content(signed_doc_name)
            
            if error:
                print(f"\n{error}")
                continue

            signature = create_signature(content, private_key)
            print(f"\nФайл '{signed_doc_name}' успішно підписано.")
            print(f"   Вміст: '{content}'")
            print(f"   Ваш підпис (хеш): {signature}")

        elif choice == '3':
            if not signature:
                print("\nПомилка: Спочатку підпишіть документ (опція 2).")
                continue
            
            filename_to_verify = input("Введіть ім'я файлу для ПЕРЕВІРКИ: ")
            content, error = get_file_content(filename_to_verify)

            if error:
                print(f"\n{error}")
                continue

            print(f"   Вміст файлу: '{content}'")
            is_valid = verify_signature(content, signature, private_key)
            
            if is_valid:
                print("\nРезультат: 'Підпис ДІЙСНИЙ'")
            else:
                print("\nРезультат: 'Підпис ПІДРОБЛЕНИЙ' (Вміст файлу змінено!)")
        
        elif choice == '4':
            print("Вихід...")
            break
        
        else:
            print("\nНевірний вибір. Будь ласка, введіть число від 1 до 4.")

if __name__ == "__main__":
    main_menu()
