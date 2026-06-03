import requests

API_URL = "http://127.0.0.1:8000/api/check"

tests = [
    ("1234567", "weak", True),
    ("12345678", "weak", True),
    ("password", "weak", True),
    ("qwerty123", "weak", True),
    ("letmein", "weak", True),
    ("monkey", "weak", True),
    ("admin", "weak", True),
    ("welcome", "weak", True),
    ("password1!", "weak", True),
    
    # === Пароли от Тиграна ===
    ("qwerty123", "weak", True),
    ("admin123", "weak", True),
    ("qwertyuiop", "weak", True),
    ("123456789", "weak", True),
    ("abc123", "weak", True),
    ("password1", "weak", True),
    ("654321", "weak", True),
    
    # === ТОЧНО НЕ В БАЗЕ (False) ===
    ("Pass1234!", "medium", False),
    ("StrongP@ss2025", "strong", False),
    ("password123", "weak", False),
    ("A1b2C3d", "weak", False),
    ("A1b2C3d!", "strong", False),
    ("A1b2C3d!E5", "strong", False),
    ("A1b2C3d!E5r", "strong", False),
    ("Password1", "medium", False),
    ("Password2024", "medium", False),
    ("aaaaa123", "weak", False),
    ("login", "weak", False),
    ("NeverLeakedPass999", "medium", False),
    ("MyUniqueP@ssw0rd", "strong", False),
    ("SuperSecureDog2025", "medium", False),
     # === ТЕСТЫ ПО ЗАДАНИЮ (из базы / не из базы) ===
    ("qwerty123", "weak", True),        # есть в базе
    ("StrongP@ss2025", "strong", False), # нет в базе
]

def run_auto_tests():
    print("АВТОМАТИЗИРОВАННЫЕ ТЕСТЫ ")
    print("=" * 65)
    
    passed = 0
    failed = 0

    for password, expected_strength, expected_leak in tests:
        display = "[пусто]" if password == "" else password
        
        try:
            response = requests.post(API_URL, json={"password": password})
            
            if response.status_code != 200:
                print(f"❌ {display} -> Ошибка: статус {response.status_code}")
                failed += 1
                continue
            
            data = response.json()
            actual_strength = data.get("strength")
            reasons = " ".join(data.get("reasons", []))
            has_leak = "утечек" in reasons
            
            strength_ok = (actual_strength == expected_strength)
            leak_ok = (has_leak == expected_leak)
            
            if strength_ok and leak_ok:
                print(f"✅ {display} -> {actual_strength} | Утечка: {has_leak}")
                passed += 1
            else:
                print(f"❌ {display} -> Ожид.: {expected_strength}, утечка={expected_leak} | Факт.: {actual_strength}, утечка={has_leak}")
                failed += 1
                
        except Exception as e:
            print(f"❌ {display} -> Ошибка соединения: {e}")
            failed += 1

    print("=" * 65)
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Не пройдено: {failed}")
    print(f"📊 Всего тестов: {len(tests)}")
    print("=" * 65)

if __name__ == "__main__":
    run_auto_tests()