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
from api_client_dtp import DTPAPIClient
from api_client_metro import MetroAPIClient


@pytest.fixture(scope="module")
def api_service():
    """Фикстура для предоставления API сервиса инцидентов"""
    return SimpleAPIService()


@pytest.fixture(scope="module")
def dtp_client():
    """Фикстура для предоставления API клиента ДТП"""
    return DTPAPIClient()


@pytest.fixture(scope="module")
def metro_client():
    """Фикстура для предоставления API клиента Метрополитен"""
    return MetroAPIClient()

