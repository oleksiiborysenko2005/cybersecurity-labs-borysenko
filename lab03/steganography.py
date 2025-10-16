from PIL import Image
import os

def text_to_binary(text):
    return ''.join(format(byte, '08b') for byte in text.encode('utf-8'))

def binary_to_text(binary):
    byte_chunks = [binary[i:i+8] for i in range(0, len(binary), 8)]
    byte_list = [int(byte, 2) for byte in byte_chunks]
    return bytearray(byte_list).decode('utf-8', errors='ignore')

def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    delimiter = "||END||"
    binary_message = text_to_binary(message + delimiter)
    message_length = len(binary_message)

    if message_length > width * height * 3:
        raise ValueError("Повідомлення занадто велике!")

    data_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            if data_index < message_length:
                r = (r & ~1) | int(binary_message[data_index]); data_index += 1
            if data_index < message_length:
                g = (g & ~1) | int(binary_message[data_index]); data_index += 1
            if data_index < message_length:
                b = (b & ~1) | int(binary_message[data_index]); data_index += 1
            
            pixels[x, y] = (r, g, b)

            if data_index >= message_length:
                img.save(output_path)
                print(f"✓ Повідомлення приховано в '{output_path}'")
                return

def extract_message(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    binary_data_list = []
    delimiter = "||END||"
    binary_delimiter = text_to_binary(delimiter)
    delimiter_len = len(binary_delimiter)

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            binary_data_list.append(str(r & 1))
            binary_data_list.append(str(g & 1))
            binary_data_list.append(str(b & 1))

            if len(binary_data_list) >= delimiter_len:
                last_bits = "".join(binary_data_list[-delimiter_len:])
                if last_bits == binary_delimiter:
                    message_binary = "".join(binary_data_list[:-delimiter_len])
                    return binary_to_text(message_binary)

    return None

if __name__ == '__main__':
    while True:
        print("\n" + "="*30)
        print("   Програма Стеганографії")
        print("="*30)
        print("1. Приховати повідомлення")
        print("2. Витягти повідомлення")
        print("3. Вихід")
        choice = input("Виберіть опцію (1, 2, 3): ")

        if choice == '1':
            try:
                input_path = input("Шлях до фото: ")
                if not os.path.exists(input_path):
                    print(f"Помилка: файл не знайдено")
                    continue
                
                message = input("Повідомлення: ")
                output_path = input("Ім'я файлу: ")
                
                hide_message(input_path, message, output_path)
            except Exception as e:
                print(f"Помилка: {e}")

        elif choice == '2':
            try:
                image_path = input("Шлях до фото: ")
                if not os.path.exists(image_path):
                    print(f"Помилка: файл не знайдено")
                    continue
                    
                extracted_message = extract_message(image_path)
                if extracted_message:
                    print(f"Повідомлення: {extracted_message}")
                else:
                    print("Повідомлення не знайдено")
            except Exception as e:
                print(f"Помилка: {e}")

        elif choice == '3':
            print("Вихід")
            break
        else:
            print("Невірний вибір")
          
