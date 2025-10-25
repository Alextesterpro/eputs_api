#!/usr/bin/env python3
"""
Общие настройки для всех тестов
"""

import pytest
import sys
import os

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_services import SimpleAPIService


@pytest.fixture(scope="module")
def api_service():
    """Фикстура для предоставления API сервиса"""
    return SimpleAPIService()


