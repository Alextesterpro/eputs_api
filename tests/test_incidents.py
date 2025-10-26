#!/usr/bin/env python3
"""
Тесты для инцидентов
"""

import pytest
from datetime import datetime


class TestIncidents:
    """Тесты для инцидентов"""
    
    def test_api_connectivity(self, api_service):
        """Тест доступности API"""
        assert api_service.is_api_available(), "API недоступен"
    
    def test_incidents_list(self, api_service):
        """Тест получения списка инцидентов"""
        result = api_service.get_all_incidents(page=1, limit=5)
        assert result is not None, "Список инцидентов не получен"
        assert "data" in result, "Нет поля data"
        assert isinstance(result["data"], list), "Данные должны быть списком"
        print("Incidents list работает")
    
    def test_incidents_get_by_id(self, api_service):
        """Тест получения инцидента по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        incidents = api_service.get_all_incidents(page=1, limit=1)
        if incidents.get("data") and len(incidents["data"]) > 0:
            incident_id = incidents["data"][0].get("id")
            if incident_id:
                result = api_service.get_incident_by_id(incident_id)
                assert result is not None, "Инцидент не получен"
                assert "data" in result, "Нет поля data"
                print("Incidents get by ID работает")
        else:
            pytest.skip("Нет инцидентов для тестирования")
    
    def test_incidents_workflow(self, api_service):
        """Тест полного workflow для инцидентов"""
        # 1. Получаем список
        incidents = api_service.get_all_incidents(page=1, limit=5)
        assert incidents is not None, "Список инцидентов не получен"
        assert "data" in incidents, "Нет поля data"
        assert isinstance(incidents["data"], list), "Данные должны быть списком"
        
        # 2. Получаем один инцидент
        if incidents.get("data") and len(incidents["data"]) > 0:
            incident_id = incidents["data"][0].get("id")
            if incident_id:
                incident = api_service.get_incident_by_id(incident_id)
                assert incident is not None, "Инцидент не получен"
                assert "data" in incident, "Нет поля data в деталях"
                assert incident["data"]["id"] == incident_id, "ID не совпадает"
        
        print("Incidents workflow работает")
    
    def test_incidents_pagination(self, api_service):
        """Тест пагинации инцидентов"""
        page1 = api_service.get_all_incidents(page=1, limit=2)
        page2 = api_service.get_all_incidents(page=2, limit=2)
        
        assert page1 is not None, "Первая страница не получена"
        assert page2 is not None, "Вторая страница не получена"
        assert "data" in page1, "Нет поля data в первой странице"
        assert "data" in page2, "Нет поля data во второй странице"
        print("Incidents pagination работает")
    
    def test_incidents_create(self, api_service):
        """Тест создания инцидента"""
        name = f"Тест {datetime.now().strftime('%H:%M:%S')}"
        description = "Простой тестовый инцидент"
        
        result = api_service.create_incident(name, description)
        assert result is not None, "Создание не работает"
        assert "data" in result, "Нет поля data"
        print("Incidents create работает")
    
    def test_incidents_update(self, api_service):
        """Тест обновления инцидента"""
        # Сначала получаем существующий инцидент
        incidents = api_service.get_all_incidents(page=1, limit=1)
        if incidents.get("data") and len(incidents["data"]) > 0:
            incident_id = incidents["data"][0].get("id")
            if incident_id:
                result = api_service.update_incident(incident_id, description="Обновлено")
                assert result is not None, "Обновление не работает"
                print("Incidents update работает")
        else:
            pytest.skip("Нет инцидентов для обновления")
    
    def test_incidents_delete(self, api_service):
        """Тест удаления инцидента"""
        # Сначала получаем существующий инцидент
        incidents = api_service.get_all_incidents(page=1, limit=1)
        if incidents.get("data") and len(incidents["data"]) > 0:
            incident_id = incidents["data"][0].get("id")
            if incident_id:
                result = api_service.delete_incident(incident_id)
                assert result is True, "Удаление не работает"
                print("Incidents delete работает")
        else:
            pytest.skip("Нет инцидентов для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
