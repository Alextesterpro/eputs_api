#!/usr/bin/env python3
"""
Простые тесты для API инцидентов
"""

from simple_api import SimpleIncidentAPI
from datetime import datetime


def test_list():
    """Тест получения списка"""
    print("🧪 Тест: Получение списка инцидентов")
    
    api = SimpleIncidentAPI()
    response = api.list_incidents(page=1, limit=5)
    
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Найдено инцидентов: {len(data.get('data', []))}")
        print("   ✅ Успешно!")
        return True
    else:
        print(f"   ❌ Ошибка: {response.text[:100]}")
        return False


def test_get():
    """Тест получения одного инцидента"""
    print("\n🧪 Тест: Получение одного инцидента")
    
    api = SimpleIncidentAPI()
    response = api.get_incident(1)  # ID = 1
    
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Название: {data.get('data', {}).get('name', 'Неизвестно')}")
        print("   ✅ Успешно!")
        return True
    else:
        print(f"   ❌ Ошибка: {response.text[:100]}")
        return False


def test_search():
    """Тест поиска"""
    print("\n🧪 Тест: Поиск инцидентов")
    
    api = SimpleIncidentAPI()
    response = api.search_incidents(page=1, limit=5)
    
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Найдено: {len(data.get('data', []))}")
        print("   ✅ Успешно!")
        return True
    else:
        print(f"   ❌ Ошибка: {response.text[:100]}")
        return False


def test_create():
    """Тест создания"""
    print("\n🧪 Тест: Создание инцидента")
    
    api = SimpleIncidentAPI()
    name = f"Тест {datetime.now().strftime('%H:%M:%S')}"
    description = "Простой тестовый инцидент"
    
    response = api.create_incident(name, description)
    
    print(f"   Статус: {response.status_code}")
    if response.status_code in [200, 201]:
        print("   ✅ Успешно!")
        return True
    else:
        print(f"   ❌ Ошибка: {response.text[:200]}")
        return False


def main():
    """Запустить все тесты"""
    print("🚀 Простые тесты API инцидентов")
    print("=" * 50)
    
    # Проверяем токен
    api = SimpleIncidentAPI()
    if not api.token:
        print("❌ Токен не найден! Запустите login_and_get_token.py")
        return
    
    print(f"✅ Токен найден: {api.token[:20]}...")
    
    # Запускаем тесты
    tests = [test_list, test_get, test_search, test_create]
    passed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
    
    print(f"\n📊 Результат: {passed}/{len(tests)} тестов прошли")
    
    if passed == len(tests):
        print("🎉 Все тесты прошли успешно!")
    else:
        print("⚠️  Некоторые тесты не прошли")


if __name__ == "__main__":
    main()
