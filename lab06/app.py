import sqlite3

def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, login TEXT, secret TEXT)")
    
    users = [
        ('user', 'Ясний день '),
        ('admin', 'СЕКРЕТНИЙ ПАРОЛЬ: 12345'),
        ('guest', 'Просто гість')
    ]
    
    cursor.executemany("INSERT INTO users (login, secret) VALUES (?, ?)", users)
    
    conn.commit()
    return conn

def run_lab():
    conn = init_db()
    cursor = conn.cursor()
    
    print("=== ЛАБОРАТОРНА: SQL Injection ===")
    print("Користувачі в базі: admin, user, guest")
    
    while True:
        print("\n" + "="*40)
        print("Підсказки для вводу:")
        print("  1. admin         (Перевірка роботи)")
        print("  2. ' OR '1'='1   (Атака/Злам)")
        print("  3. exit          (Вихід)")
        print("="*40)
        
        target = input("Поле для вводу > ").strip()
        
        if target == 'exit': break
        if not target: continue

        # --- ВРАЗЛИВИЙ ВАРІАНТ ---
        sql_vuln = f"SELECT * FROM users WHERE login = '{target}'"
        print(f"\n[1] ВРАЗЛИВИЙ ЗАПИТ:  {sql_vuln}")
        
        try:
            cursor.execute(sql_vuln)
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(f"   [+] ЗНАЙДЕНО: {row[1]} | Інфо: {row[2]}")
            else:
                print("   [-] Нічого не знайдено.")
        except Exception as e:
            print(f"   [!] ПОМИЛКА SQL: {e}")

        # --- ЗАХИЩЕНИЙ ВАРІАНТ ---
        sql_sec = "SELECT * FROM users WHERE login = ?"
        print(f"\n[2] ЗАХИЩЕНИЙ ЗАПИТ:  {sql_sec}  [Параметр: '{target}']")
        
        try:
            cursor.execute(sql_sec, (target,))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(f"   [+] ЗНАЙДЕНО: {row[1]} | Інфо: {row[2]}")
            else:
                print("   [-] Нічого не знайдено (Атака заблокована).")
        except Exception as e:
            print(f"   [!] ПОМИЛКА: {e}")

if __name__ == "__main__":
    run_lab()
