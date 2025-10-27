#!/usr/bin/env python3
"""
Тесты для ключевых слов
"""

import pytest
from datetime import datetime


class TestKeywords:
    """Тесты для ключевых слов"""
    
    def test_keywords_list(self, api_service):
        """Тест получения списка ключевых слов"""
        result = api_service.get_all_keywords()
        assert result is not None, "Список ключевых слов не получен"
        assert "data" in result, "Нет поля data"
        assert isinstance(result["data"], list), "Данные должны быть списком"
        print("Keywords list работает")
    
    def test_keywords_get_by_id(self, api_service):
        """Тест получения ключевого слова по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        keywords = api_service.get_all_keywords()
        if keywords.get("data") and len(keywords["data"]) > 0:
            keyword_id = keywords["data"][0].get("id")
            if keyword_id:
                result = api_service.get_keyword_by_id(keyword_id)
                assert result is not None, "Ключевое слово не получено"
                assert "data" in result, "Нет поля data"
                print("Keywords get by ID работает")
        else:
            pytest.skip("Нет ключевых слов для тестирования")
    
    def test_keywords_workflow(self, api_service):
        """Тест полного workflow для ключевых слов"""
        # 1. Получаем список
        keywords = api_service.get_all_keywords()
        assert keywords is not None, "Список ключевых слов не получен"
        assert "data" in keywords, "Нет поля data"
        assert isinstance(keywords["data"], list), "Данные должны быть списком"
        
        # 2. Получаем одно ключевое слово
        if keywords.get("data") and len(keywords["data"]) > 0:
            keyword_id = keywords["data"][0].get("id")
            if keyword_id:
                keyword = api_service.get_keyword_by_id(keyword_id)
                assert keyword is not None, "Ключевое слово не получено"
                assert "data" in keyword, "Нет поля data в деталях"
                assert keyword["data"]["id"] == keyword_id, "ID не совпадает"
        
        print("Keywords workflow работает")
    
    def test_keywords_create(self, api_service):
        """Тест создания ключевого слова"""
        name = f"Тест ключевое слово {datetime.now().strftime('%H:%M:%S')}"
        description = "Простое тестовое ключевое слово"
        
        result = api_service.create_keyword(name, description)
        assert result is not None, "Создание не работает"
        assert "data" in result, "Нет поля data"
        print("Keywords create работает")
    
    def test_keywords_update(self, api_service):
        """Тест обновления ключевого слова"""
        # Сначала получаем существующее ключевое слово
        keywords = api_service.get_all_keywords()
        if keywords.get("data") and len(keywords["data"]) > 0:
            keyword_id = keywords["data"][0].get("id")
            if keyword_id:
                result = api_service.update_keyword(keyword_id, description="Обновлено")
                assert result is not None, "Обновление не работает"
                print("Keywords update работает")
        else:
            pytest.skip("Нет ключевых слов для обновления")
    
    def test_keywords_delete(self, api_service):
        """Тест удаления ключевого слова"""
        # Сначала получаем существующее ключевое слово
        keywords = api_service.get_all_keywords()
        if keywords.get("data") and len(keywords["data"]) > 0:
            keyword_id = keywords["data"][0].get("id")
            if keyword_id:
                result = api_service.delete_keyword(keyword_id)
                assert result is True, "Удаление не работает"
                print("Keywords delete работает")
        else:
            pytest.skip("Нет ключевых слов для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
