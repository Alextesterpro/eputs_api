#!/usr/bin/env python3
"""
Тесты для событий
"""

import pytest
from datetime import datetime


class TestEvents:
    """Тесты для событий"""
    
    def test_events_list(self, api_service):
        """Тест получения списка событий"""
        result = api_service.get_all_events()
        assert result is not None, "Список событий не получен"
        assert "data" in result, "Нет поля data"
        assert isinstance(result["data"], list), "Данные должны быть списком"
        print("Events list работает")
    
    def test_events_get_by_id(self, api_service):
        """Тест получения события по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        events = api_service.get_all_events()
        if events.get("data") and len(events["data"]) > 0:
            event_id = events["data"][0].get("id")
            if event_id:
                result = api_service.get_event_by_id(event_id)
                assert result is not None, "Событие не получено"
                assert "data" in result, "Нет поля data"
                print("Events get by ID работает")
        else:
            pytest.skip("Нет событий для тестирования")
    
    def test_events_workflow(self, api_service):
        """Тест полного workflow для событий"""
        # 1. Получаем список
        events = api_service.get_all_events()
        assert events is not None, "Список событий не получен"
        assert "data" in events, "Нет поля data"
        assert isinstance(events["data"], list), "Данные должны быть списком"
        
        # 2. Получаем одно событие
        if events.get("data") and len(events["data"]) > 0:
            event_id = events["data"][0].get("id")
            if event_id:
                event = api_service.get_event_by_id(event_id)
                assert event is not None, "Событие не получено"
                assert "data" in event, "Нет поля data в деталях"
                assert event["data"]["id"] == event_id, "ID не совпадает"
        
        print("Events workflow работает")
    
    def test_events_create(self, api_service):
        """Тест создания события"""
        name = f"Тест событие {datetime.now().strftime('%H:%M:%S')}"
        description = "Простое тестовое событие"
        
        result = api_service.create_event(name, description)
        assert result is not None, "Создание не работает"
        assert "data" in result, "Нет поля data"
        print("Events create работает")
    
    def test_events_update(self, api_service):
        """Тест обновления события"""
        # Сначала получаем существующее событие
        events = api_service.get_all_events()
        if events.get("data") and len(events["data"]) > 0:
            event_id = events["data"][0].get("id")
            if event_id:
                result = api_service.update_event(event_id, description="Обновлено")
                assert result is not None, "Обновление не работает"
                print("Events update работает")
        else:
            pytest.skip("Нет событий для обновления")
    
    def test_events_delete(self, api_service):
        """Тест удаления события"""
        # Сначала получаем существующее событие
        events = api_service.get_all_events()
        if events.get("data") and len(events["data"]) > 0:
            event_id = events["data"][0].get("id")
            if event_id:
                result = api_service.delete_event(event_id)
                assert result is True, "Удаление не работает"
                print("Events delete работает")
        else:
            pytest.skip("Нет событий для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
