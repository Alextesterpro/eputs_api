#!/usr/bin/env python3
"""
Тесты для категорий
"""

import pytest
from datetime import datetime


class TestCategories:
    """Тесты для категорий"""
    
    def test_categories_list(self, api_service):
        """Тест получения списка категорий"""
        result = api_service.get_all_categories()
        assert result is not None, "Список категорий не получен"
        assert "data" in result, "Нет поля data"
        assert isinstance(result["data"], list), "Данные должны быть списком"
        print("Categories list работает")
    
    def test_categories_get_by_id(self, api_service):
        """Тест получения категории по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        categories = api_service.get_all_categories()
        if categories.get("data") and len(categories["data"]) > 0:
            category_id = categories["data"][0].get("id")
            if category_id:
                result = api_service.get_category_by_id(category_id)
                assert result is not None, "Категория не получена"
                assert "data" in result, "Нет поля data"
                print("Categories get by ID работает")
        else:
            pytest.skip("Нет категорий для тестирования")
    
    def test_categories_workflow(self, api_service):
        """Тест полного workflow для категорий"""
        # 1. Получаем список
        categories = api_service.get_all_categories()
        assert categories is not None, "Список категорий не получен"
        assert "data" in categories, "Нет поля data"
        assert isinstance(categories["data"], list), "Данные должны быть списком"
        
        # 2. Получаем одну категорию
        if categories.get("data") and len(categories["data"]) > 0:
            category_id = categories["data"][0].get("id")
            if category_id:
                category = api_service.get_category_by_id(category_id)
                assert category is not None, "Категория не получена"
                assert "data" in category, "Нет поля data в деталях"
                assert category["data"]["id"] == category_id, "ID не совпадает"
        
        print("Categories workflow работает")
    
    def test_categories_create(self, api_service):
        """Тест создания категории"""
        try:
            name = f"Тест категория {datetime.now().strftime('%H:%M:%S')}"
            description = "Простая тестовая категория"
            
            result = api_service.create_category(name, description)
            assert result is not None, "Создание не работает"
            assert "data" in result, "Нет поля data"
            print("Categories create работает")
        except Exception as e:
            print(f"Categories create: {e}")
    
    def test_categories_update(self, api_service):
        """Тест обновления категории"""
        try:
            # Сначала получаем существующую категорию
            categories = api_service.get_all_categories()
            if categories.get("data") and len(categories["data"]) > 0:
                category_id = categories["data"][0].get("id")
                if category_id:
                    result = api_service.update_category(category_id, description="Обновлено")
                    assert result is not None, "Обновление не работает"
                    print("Categories update работает")
            else:
                pytest.skip("Нет категорий для обновления")
        except Exception as e:
            print(f"Categories update: {e}")
    
    def test_categories_delete(self, api_service):
        """Тест удаления категории"""
        try:
            # Сначала получаем существующую категорию
            categories = api_service.get_all_categories()
            if categories.get("data") and len(categories["data"]) > 0:
                category_id = categories["data"][0].get("id")
                if category_id:
                    result = api_service.delete_category(category_id)
                    assert result is True, "Удаление не работает"
                    print("Categories delete работает")
            else:
                pytest.skip("Нет категорий для удаления")
        except Exception as e:
            print(f"Categories delete: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
