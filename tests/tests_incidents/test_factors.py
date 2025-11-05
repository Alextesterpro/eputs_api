#!/usr/bin/env python3
"""
Тесты для пользовательских факторов инцидентов
"""

import pytest
from datetime import datetime


class TestFactors:
    """Тесты для пользовательских факторов инцидентов"""
    
    def test_factors_list(self, incidents_client):
        """Тест получения списка факторов"""
        result = incidents_client.get_factors_list()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        assert isinstance(data["data"], list), "Данные должны быть списком"
        print("Factors list работает")
    
    def test_factors_get_by_id(self, incidents_client):
        """Тест получения фактора по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        factors = incidents_client.get_factors_list()
        if factors.status_code == 200:
            data = factors.json()
            if data.get("data") and len(data["data"]) > 0:
                factor_id = data["data"][0].get("id")
            if factor_id:
                    result = incidents_client.get_factor_by_id(factor_id)
                    assert result.status_code == 200, f"Status code: {result.status_code}"
                    response_data = result.json()
                    assert "data" in response_data, "Нет поля data"
                print("Factors get by ID работает")
                    return
            pytest.skip("Нет факторов для тестирования")
    
    def test_factors_pagination(self, incidents_client):
        """Тест пагинации факторов"""
        page1 = incidents_client.get_factors_list(page=1, limit=5)
        page2 = incidents_client.get_factors_list(page=2, limit=5)
        
        assert page1.status_code == 200, f"Page 1 status: {page1.status_code}"
        assert page2.status_code == 200, f"Page 2 status: {page2.status_code}"
        
        data1 = page1.json()
        data2 = page2.json()
        
        assert "data" in data1, "Нет поля data в первой странице"
        assert "data" in data2, "Нет поля data во второй странице"
        print("Factors pagination работает")
    
    def test_factors_create(self, incidents_client):
        """Тест создания фактора"""
        name = f"Фактор_апи_тест_{datetime.now().strftime('%H%M%S')}"
        is_geo = True
        
        result = incidents_client.create_factor(name, is_geo)
        assert result.status_code in [200, 201], f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        print("Factors create работает")
    
    def test_factors_update(self, incidents_client):
        """Тест обновления фактора"""
            # Сначала получаем существующий фактор
        factors = incidents_client.get_factors_list()
        if factors.status_code == 200:
            data = factors.json()
            if data.get("data") and len(data["data"]) > 0:
                factor_id = data["data"][0].get("id")
                if factor_id:
                    result = incidents_client.update_factor(factor_id, name="Фактор_апи_тест_изменение", is_geo=True)
                    # Проверяем системный фактор
                    if result.status_code == 422 and "is_system" in result.text:
                        pytest.skip("Системный фактор нельзя изменять - это нормально")
                    assert result.status_code in [200, 201], f"Status code: {result.status_code}"
                    print("Factors update работает")
                    return
                pytest.skip("Нет факторов для обновления")
    
    def test_factors_delete(self, incidents_client):
        """Тест удаления фактора"""
            # Сначала получаем существующий фактор
        factors = incidents_client.get_factors_list()
        if factors.status_code == 200:
            data = factors.json()
            if data.get("data") and len(data["data"]) > 0:
                factor_id = data["data"][0].get("id")
                if factor_id:
                    result = incidents_client.delete_factor(factor_id)
                    # Проверяем системный фактор
                    if result.status_code == 422 and "is_system" in result.text:
                        pytest.skip("Системный фактор нельзя удалять - это нормально")
                    assert result.status_code in [200, 204], f"Status code: {result.status_code}"
                    print("Factors delete работает")
                    return
                pytest.skip("Нет факторов для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
