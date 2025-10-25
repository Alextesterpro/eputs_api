#!/usr/bin/env python3
"""
Скрипт для запуска тестов
Следует принципам POM и лучшим практикам
"""

import subprocess
import sys
import os
from datetime import datetime


def check_environment():
    """Проверить окружение"""
    print("🔍 Проверка окружения...")
    
    # Проверяем наличие токена
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("Запустите сначала: python3 simple_login.py")
        return False
    
    # Проверяем наличие токена в файле
    with open('.env', 'r') as f:
        content = f.read()
        if 'EPUTS_TOKEN=' not in content:
            print("❌ Токен не найден в .env файле!")
            print("Запустите сначала: python3 simple_login.py")
            return False
    
    print("✅ Окружение готово")
    return True


def run_tests():
    """Запустить тесты"""
    print("🚀 Запуск тестов...")
    
    # Команда для запуска pytest
    cmd = [
        sys.executable, "-m", "pytest",
        "test_incidents.py",
        "-v",  # подробный вывод
        "--tb=short",  # короткий traceback
        "--strict-markers",  # строгие маркеры
        "--disable-warnings",  # отключить предупреждения
        "--color=yes"  # цветной вывод
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("📊 Результаты тестов:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Предупреждения:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Ошибка запуска тестов: {e}")
        return False


def generate_report():
    """Сгенерировать отчет"""
    print("📝 Генерация отчета...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"test_report_{timestamp}.html"
    
    cmd = [
        sys.executable, "-m", "pytest",
        "test_incidents.py",
        "--html", report_file,
        "--self-contained-html"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Отчет сохранен: {report_file}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Ошибка генерации отчета")
        return False


def main():
    """Главная функция"""
    print("🧪 Запуск тестов API инцидентов")
    print("=" * 50)
    
    # Проверяем окружение
    if not check_environment():
        return 1
    
    # Запускаем тесты
    if not run_tests():
        print("❌ Тесты не прошли")
        return 1
    
    # Генерируем отчет
    generate_report()
    
    print("🎉 Все готово!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)