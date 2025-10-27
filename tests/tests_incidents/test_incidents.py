#!/usr/bin/env python3
"""
Тесты для инцидентов
"""

import pytest
from datetime import datetime


class TestIncidents:
    """Тесты для инцидентов"""
    
    def test_incidents_list(self, incidents_client):
        """Тест получения списка инцидентов"""
        result = incidents_client.get_incidents_list(page=1, limit=5)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        assert isinstance(data["data"], list), "Данные должны быть списком"
        print("Incidents list работает")
    
    def test_incidents_get_by_id(self, incidents_client):
        """Тест получения инцидента по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        incidents = incidents_client.get_incidents_list(page=1, limit=1)
        if incidents.status_code == 200:
            data = incidents.json()
            if data.get("data") and len(data["data"]) > 0:
                incident_id = data["data"][0].get("id")
                if incident_id:
                    result = incidents_client.get_incident_by_id(incident_id)
                    assert result.status_code == 200, f"Status code: {result.status_code}"
                    response_data = result.json()
                    assert "data" in response_data, "Нет поля data"
                    print("Incidents get by ID работает")
                    return
        pytest.skip("Нет инцидентов для тестирования")
    
    def test_incidents_pagination(self, incidents_client):
        """Тест пагинации инцидентов"""
        page1 = incidents_client.get_incidents_list(page=1, limit=2)
        page2 = incidents_client.get_incidents_list(page=2, limit=2)
        
        assert page1.status_code == 200, f"Page 1 status: {page1.status_code}"
        assert page2.status_code == 200, f"Page 2 status: {page2.status_code}"
        
        data1 = page1.json()
        data2 = page2.json()
        
        assert "data" in data1, "Нет поля data в первой странице"
        assert "data" in data2, "Нет поля data во второй странице"
        print("Incidents pagination работает")
    
    def test_incidents_create(self, incidents_client):
        """Тест создания инцидента"""
        name = f"Тест {datetime.now().strftime('%H:%M:%S')}"
        description = "Простой тестовый инцидент"
        
        result = incidents_client.create_incident(name, description)
        assert result.status_code in [200, 201], f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        print("Incidents create работает")
    
    def test_incidents_update(self, incidents_client):
        """Тест обновления инцидента"""
        # Сначала получаем существующий инцидент
        incidents = incidents_client.get_incidents_list(page=1, limit=1)
        if incidents.status_code == 200:
            data = incidents.json()
            if data.get("data") and len(data["data"]) > 0:
                incident_id = data["data"][0].get("id")
                if incident_id:
                    result = incidents_client.update_incident(incident_id, description="Обновлено")
                    assert result.status_code in [200, 201], f"Status code: {result.status_code}"
                    print("Incidents update работает")
                    return
        pytest.skip("Нет инцидентов для обновления")
    
    def test_incidents_delete(self, incidents_client):
        """Тест удаления инцидента"""
        # Сначала получаем существующий инцидент
        incidents = incidents_client.get_incidents_list(page=1, limit=1)
        if incidents.status_code == 200:
            data = incidents.json()
            if data.get("data") and len(data["data"]) > 0:
                incident_id = data["data"][0].get("id")
                if incident_id:
                    result = incidents_client.delete_incident(incident_id)
                    assert result.status_code in [200, 204], f"Status code: {result.status_code}"
                    print("Incidents delete работает")
                    return
        pytest.skip("Нет инцидентов для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
