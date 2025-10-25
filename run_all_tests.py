#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов
"""

import pytest
import sys
import os

def main():
    """Запуск всех тестов"""
    print("🚀 Запуск всех тестов...")
    print("=" * 50)
    
    # Запуск всех тестов в папке tests/
    result = pytest.main([
        "tests/",
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    
    print("=" * 50)
    if result == 0:
        print("✅ Все тесты прошли успешно!")
    else:
        print("❌ Некоторые тесты не прошли")
    
    return result

if __name__ == "__main__":
    sys.exit(main())
