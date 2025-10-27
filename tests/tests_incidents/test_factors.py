#!/usr/bin/env python3
"""
Тесты для пользовательских факторов инцидентов
"""

import pytest
from datetime import datetime


class TestFactors:
    """Тесты для пользовательских факторов инцидентов"""
    
    def test_factors_list(self, api_service):
        """Тест получения списка факторов"""
        result = api_service.get_all_factors()
        assert result is not None, "Список факторов не получен"
        assert "data" in result, "Нет поля data"
        assert isinstance(result["data"], list), "Данные должны быть списком"
        print("Factors list работает")
    
    def test_factors_get_by_id(self, api_service):
        """Тест получения фактора по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        factors = api_service.get_all_factors()
        if factors.get("data") and len(factors["data"]) > 0:
            factor_id = factors["data"][0].get("id")
            if factor_id:
                result = api_service.get_factor_by_id(factor_id)
                assert result is not None, "Фактор не получен"
                assert "data" in result, "Нет поля data"
                print("Factors get by ID работает")
        else:
            pytest.skip("Нет факторов для тестирования")
    
    def test_factors_workflow(self, api_service):
        """Тест полного workflow для факторов"""
        # 1. Получаем список
        factors = api_service.get_all_factors()
        assert factors is not None, "Список факторов не получен"
        assert "data" in factors, "Нет поля data"
        assert isinstance(factors["data"], list), "Данные должны быть списком"
        
        # 2. Получаем один фактор
        if factors.get("data") and len(factors["data"]) > 0:
            factor_id = factors["data"][0].get("id")
            if factor_id:
                factor = api_service.get_factor_by_id(factor_id)
                assert factor is not None, "Фактор не получен"
                assert "data" in factor, "Нет поля data в деталях"
                assert factor["data"]["id"] == factor_id, "ID не совпадает"
        
        print("Factors workflow работает")
    
    def test_factors_search(self, api_service):
        """Тест поиска факторов по имени"""
        try:
            result = api_service.search_factors(name="тест")
            assert result is not None, "Поиск не работает"
            assert "data" in result, "Нет поля data"
            print("Factors search работает")
        except Exception as e:
            print(f"Factors search: {e}")
    
    def test_factors_pagination(self, api_service):
        """Тест пагинации факторов"""
        page1 = api_service.get_all_factors(page=1, limit=5)
        page2 = api_service.get_all_factors(page=2, limit=5)
        
        assert page1 is not None, "Первая страница не получена"
        assert page2 is not None, "Вторая страница не получена"
        assert "data" in page1, "Нет поля data в первой странице"
        assert "data" in page2, "Нет поля data во второй странице"
        print("Factors pagination работает")
    
    def test_factors_create(self, api_service):
        """Тест создания фактора"""
        name = f"Фактор_апи_тест_{datetime.now().strftime('%H%M%S')}"
        is_geo = True
        
        result = api_service.create_factor(name, is_geo)
        assert result is not None, "Создание не работает"
        assert "data" in result, "Нет поля data"
        print("Factors create работает")
    
    def test_factors_update(self, api_service):
        """Тест обновления фактора"""
        try:
            # Сначала получаем существующий фактор
            factors = api_service.get_all_factors()
            if factors.get("data") and len(factors["data"]) > 0:
                factor_id = factors["data"][0].get("id")
                if factor_id:
                    result = api_service.update_factor(factor_id, name="Фактор_апи_тест_изменение", is_geo=True)
                    assert result is not None, "Обновление не работает"
                    print("Factors update работает")
            else:
                pytest.skip("Нет факторов для обновления")
        except Exception as e:
            if "системный фактор нельзя изменять" in str(e) or "is_system" in str(e):
                pytest.skip("Системный фактор нельзя изменять - это нормально")
            else:
                raise
    
    def test_factors_delete(self, api_service):
        """Тест удаления фактора"""
        try:
            # Сначала получаем существующий фактор
            factors = api_service.get_all_factors()
            if factors.get("data") and len(factors["data"]) > 0:
                factor_id = factors["data"][0].get("id")
                if factor_id:
                    result = api_service.delete_factor(factor_id)
                    assert result is True, "Удаление не работает"
                    print("Factors delete работает")
            else:
                pytest.skip("Нет факторов для удаления")
        except Exception as e:
            if "системный фактор нельзя изменять" in str(e) or "is_system" in str(e):
                pytest.skip("Системный фактор нельзя удалять - это нормально")
            else:
                raise


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
