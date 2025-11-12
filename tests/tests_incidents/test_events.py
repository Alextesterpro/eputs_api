#!/usr/bin/env python3
"""
Тесты для событий
"""

import pytest
from datetime import datetime


class TestEvents:
    """Тесты для событий"""
    
    def test_events_list(self, incidents_client):
        """Тест получения списка событий"""
        result = incidents_client.get_events_list()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        assert isinstance(data["data"], list), "Данные должны быть списком"
        print("Events list работает")
    
    def test_events_get_by_id(self, incidents_client):
        """Тест получения события по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        events = incidents_client.get_events_list()
        if events.status_code == 200:
            data = events.json()
            if data.get("data") and len(data["data"]) > 0:
                event_id = data["data"][0].get("id")
            if event_id:
                result = incidents_client.get_event_by_id(event_id)
                assert result.status_code == 200, f"Status code: {result.status_code}"
                response_data = result.json()
                assert "data" in response_data, "Нет поля data"
                print("Events get by ID работает")
                return
            pytest.skip("Нет событий для тестирования")
    
    def test_events_create(self, incidents_client):
        """Тест создания события"""
        name = f"Тест событие {datetime.now().strftime('%H:%M:%S')}"
        description = "Простое тестовое событие"
        
        result = incidents_client.create_event(name, description)
        assert result.status_code in [200, 201], f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        print("Events create работает")
    
    def test_events_update(self, incidents_client):
        """Тест обновления события"""
        # Сначала получаем существующее событие
        events = incidents_client.get_events_list()
        if events.status_code == 200:
            data = events.json()
            if data.get("data") and len(data["data"]) > 0:
                event_id = data["data"][0].get("id")
            if event_id:
                result = incidents_client.update_event(event_id, description="Обновлено")
                assert result.status_code in [200, 201], f"Status code: {result.status_code}"
                print("Events update работает")
                return
            pytest.skip("Нет событий для обновления")
    
    def test_events_delete(self, incidents_client):
        """Тест удаления события"""
        # Сначала получаем существующее событие
        events = incidents_client.get_events_list()
        if events.status_code == 200:
            data = events.json()
            if data.get("data") and len(data["data"]) > 0:
                event_id = data["data"][0].get("id")
            if event_id:
                result = incidents_client.delete_event(event_id)
                assert result.status_code in [200, 204], f"Status code: {result.status_code}"
                print("Events delete работает")
                return
            pytest.skip("Нет событий для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
