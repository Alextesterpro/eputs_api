#!/usr/bin/env python3
"""
Тесты для категорий
"""

import pytest
from datetime import datetime


class TestCategories:
    """Тесты для категорий"""
    
    def test_categories_list(self, incidents_client):
        """Тест получения списка категорий"""
        result = incidents_client.get_categories_list()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        assert isinstance(data["data"], list), "Данные должны быть списком"
        print("Categories list работает")
    
    def test_categories_get_by_id(self, incidents_client):
        """Тест получения категории по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        categories = incidents_client.get_categories_list()
        if categories.status_code == 200:
            data = categories.json()
            if data.get("data") and len(data["data"]) > 0:
                category_id = data["data"][0].get("id")
            if category_id:
                    result = incidents_client.get_category_by_id(category_id)
                    assert result.status_code == 200, f"Status code: {result.status_code}"
                    response_data = result.json()
                    assert "data" in response_data, "Нет поля data"
                print("Categories get by ID работает")
                    return
            pytest.skip("Нет категорий для тестирования")
    
    def test_categories_create(self, incidents_client):
        """Тест создания категории"""
        name = f"Тест категория {datetime.now().strftime('%H:%M:%S')}"
        description = "Простая тестовая категория"
        
        result = incidents_client.create_category(name, description)
        assert result.status_code in [200, 201], f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        print("Categories create работает")
    
    def test_categories_update(self, incidents_client):
        """Тест обновления категории"""
        # Сначала получаем существующую категорию
        categories = incidents_client.get_categories_list()
        if categories.status_code == 200:
            data = categories.json()
            if data.get("data") and len(data["data"]) > 0:
                category_id = data["data"][0].get("id")
            if category_id:
                    result = incidents_client.update_category(category_id, description="Обновлено")
                    assert result.status_code in [200, 201], f"Status code: {result.status_code}"
                print("Categories update работает")
                    return
            pytest.skip("Нет категорий для обновления")
    
    def test_categories_delete(self, incidents_client):
        """Тест удаления категории"""
        # Сначала получаем существующую категорию
        categories = incidents_client.get_categories_list()
        if categories.status_code == 200:
            data = categories.json()
            if data.get("data") and len(data["data"]) > 0:
                category_id = data["data"][0].get("id")
            if category_id:
                    result = incidents_client.delete_category(category_id)
                    assert result.status_code in [200, 204], f"Status code: {result.status_code}"
                print("Categories delete работает")
                    return
            pytest.skip("Нет категорий для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
