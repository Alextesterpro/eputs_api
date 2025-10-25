#!/usr/bin/env python3
"""
Тесты для общей информации об API
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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
