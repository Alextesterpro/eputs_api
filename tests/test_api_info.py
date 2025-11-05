#!/usr/bin/env python3
"""
Тесты для общей информации об API и проверки токена
"""

import pytest
from datetime import datetime


class TestAPIInfo:
    """Тесты для общей информации об API"""
    
    def test_token_validation(self, incidents_client):
        """Тест валидации токена"""
        token = incidents_client._get_token()
        assert token is not None, "Токен не найден"
        assert len(token) > 10, "Токен слишком короткий"
        print("Token validation работает")
    
    def test_headers_validation(self, incidents_client):
        """Тест валидации заголовков"""
        headers = incidents_client._get_headers()
        assert "Authorization" in headers, "Нет заголовка Authorization"
        assert "Content-Type" in headers, "Нет заголовка Content-Type"
        assert "project" in headers, "Нет заголовка project"
        assert "service" in headers, "Нет заголовка service"
        print("Headers validation работает")


class TestTokenCheck:
    """Тесты для проверки валидности токена через реальные API запросы"""
    
    def test_incidents_token_check(self, incidents_client):
        """Проверка токена через API инцидентов"""
        result = incidents_client.check_token()
        
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
    
    def test_parking_token_check(self, parking_client):
        """Проверка токена через API Парковочное пространство"""
        result = parking_client.check_token()
        
        print(f"\nРезультат проверки токена (Parking):")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        assert result['valid'] is True, f"Токен невалиден: {result['message']}"
        assert result['status_code'] in [200, 201], f"Неожиданный статус код: {result['status_code']}"
    
    def test_digital_twin_token_check(self, digital_twin_client):
        """Проверка токена через API Цифровой двойник"""
        result = digital_twin_client.check_token()
        
        print(f"\nРезультат проверки токена (Digital Twin):")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        assert result['valid'] is True, f"Токен невалиден: {result['message']}"
        assert result['status_code'] in [200, 201], f"Неожиданный статус код: {result['status_code']}"
    
    def test_external_transport_token_check(self, external_transport_client):
        """Проверка токена через API Внешний транспорт"""
        result = external_transport_client.check_token()
        
        print(f"\nРезультат проверки токена (External Transport):")
        print(f"  Валиден: {result['valid']}")
        print(f"  Статус код: {result['status_code']}")
        print(f"  Сообщение: {result['message']}")
        
        assert result['valid'] is True, f"Токен невалиден: {result['message']}"
        assert result['status_code'] in [200, 201], f"Неожиданный статус код: {result['status_code']}"
    
    def test_water_transport_token_check(self, water_transport_client):
        """Проверка токена через API Водного транспорта"""
        result = water_transport_client.check_token()
        
        print(f"\nРезультат проверки токена (Water Transport):")
        print(f"  Валиден: {result}")
        
        assert result is True, "Токен невалиден для Water Transport API"
    
    def test_token_unauthorized_simulation(self, incidents_client):
        """Симуляция проверки с невалидным токеном (опционально)"""
        original_token = incidents_client.token
        
        try:
            incidents_client.token = "INVALID_TOKEN_12345"
            incidents_client.headers = incidents_client._get_headers()
            
            result = incidents_client.check_token()
            
            print(f"\nРезультат проверки невалидного токена:")
            print(f"  Валиден: {result['valid']}")
            print(f"  Статус код: {result['status_code']}")
            print(f"  Сообщение: {result['message']}")
            
            assert result['valid'] is False, "Невалидный токен был принят как валидный!"
            assert result['status_code'] == 401, f"Ожидался 401, получен {result['status_code']}"
            
        finally:
            incidents_client.token = original_token
            incidents_client.headers = incidents_client._get_headers()
    
    def test_passenger_transport_token_check(self, passenger_transport_client):
        """Проверка токена для Passenger Transport API"""
        result = passenger_transport_client.check_token()
        
        print(f"\nПассажирский транспорт API:")
        print(f"  Токен валиден: {result}")
        
        assert result is True, "Токен должен быть валидным!"
    
    def test_data_bus_token_check(self, data_bus_client):
        """Проверка токена для Data Bus API"""
        result = data_bus_client.check_token()
        
        print(f"\nData Bus (Общая шина) API:")
        print(f"  Токен валиден: {result}")
        
        assert result is True, "Токен должен быть валидным!"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
