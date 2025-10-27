#!/usr/bin/env python3
"""
Тесты для общей информации об API и проверки токена
"""

import pytest
from datetime import datetime


class TestAPIInfo:
    """Тесты для общей информации об API"""
    
    def test_api_connectivity(self, api_service):
        """Тест доступности API"""
        assert api_service.is_api_available(), "API недоступен"
        print("API connectivity работает")
    
    def test_token_validation(self, api_service):
        """Тест валидации токена"""
        token = api_service.client._get_token()
        assert token is not None, "Токен не найден"
        assert len(token) > 10, "Токен слишком короткий"
        print("Token validation работает")
    
    def test_headers_validation(self, api_service):
        """Тест валидации заголовков"""
        headers = api_service.client._get_headers()
        assert "Authorization" in headers, "Нет заголовка Authorization"
        assert "Content-Type" in headers, "Нет заголовка Content-Type"
        assert "project" in headers, "Нет заголовка project"
        assert "service" in headers, "Нет заголовка service"
        print("Headers validation работает")
    
    def test_api_info(self, api_service):
        """Тест получения информации о состоянии API и токена"""
        token_available = api_service.client._get_token() is not None
        api_available = api_service.is_api_available()
        
        assert token_available, "Токен не найден в .env или не установлен"
        assert api_available, "API недоступен или возвращает ошибку"
        
        print("API info работает")


class TestTokenCheck:
    """Тесты для проверки валидности токена через реальные API запросы"""
    
    def test_incidents_token_check(self, api_service):
        """Проверка токена через API инцидентов"""
        result = api_service.client.check_token()
        
        print(f"\nРезультат проверки токена (Incidents):")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        assert result['valid'] is True, f"Токен невалиден: {result['message']}"
        assert result['status_code'] in [200, 201], f"Неожиданный статус код: {result['status_code']}"
    
    def test_dtp_token_check(self, dtp_client):
        """Проверка токена через API ДТП"""
        result = dtp_client.check_token()
        
        print(f"\nРезультат проверки токена (DTP):")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        assert result['valid'] is True, f"Токен невалиден: {result['message']}"
        assert result['status_code'] in [200, 201], f"Неожиданный статус код: {result['status_code']}"
    
    def test_metro_token_check(self, metro_client):
        """Проверка токена через API Метрополитен"""
        result = metro_client.check_token()
        
        print(f"\nРезультат проверки токена (Metro):")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        assert result['valid'] is True, f"Токен невалиден: {result['message']}"
        assert result['status_code'] in [200, 201], f"Неожиданный статус код: {result['status_code']}"
    
    def test_token_unauthorized_simulation(self, api_service):
        """Симуляция проверки с невалидным токеном (опционально)"""
        original_token = api_service.client.token
        
        try:
            api_service.client.token = "INVALID_TOKEN_12345"
            api_service.client.headers = api_service.client._get_headers()
            
            result = api_service.client.check_token()
            
            print(f"\nРезультат проверки невалидного токена:")
            print(f"  Валиден: {result['valid']}")
            print(f"  Статус код: {result['status_code']}")
            print(f"  Сообщение: {result['message']}")
            
            assert result['valid'] is False, "Невалидный токен был принят как валидный!"
            assert result['status_code'] == 401, f"Ожидался 401, получен {result['status_code']}"
            
        finally:
            api_service.client.token = original_token
            api_service.client.headers = api_service.client._get_headers()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
