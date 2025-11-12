#!/usr/bin/env python3
"""
Тесты для ключевых слов
"""

import pytest
from datetime import datetime


class TestKeywords:
    """Тесты для ключевых слов"""
    
    def test_keywords_list(self, incidents_client):
        """Тест получения списка ключевых слов"""
        result = incidents_client.get_keywords_list()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        assert isinstance(data["data"], list), "Данные должны быть списком"
        print("Keywords list работает")
    
    def test_keywords_get_by_id(self, incidents_client):
        """Тест получения ключевого слова по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        keywords = incidents_client.get_keywords_list()
        if keywords.status_code == 200:
            data = keywords.json()
            if data.get("data") and len(data["data"]) > 0:
                keyword_id = data["data"][0].get("id")
            if keyword_id:
                result = incidents_client.get_keyword_by_id(keyword_id)
                assert result.status_code == 200, f"Status code: {result.status_code}"
                response_data = result.json()
                assert "data" in response_data, "Нет поля data"
                print("Keywords get by ID работает")
                return
            pytest.skip("Нет ключевых слов для тестирования")
    
    def test_keywords_create(self, incidents_client):
        """Тест создания ключевого слова"""
        name = f"Тест ключевое слово {datetime.now().strftime('%H:%M:%S')}"
        description = "Простое тестовое ключевое слово"
        
        result = incidents_client.create_keyword(name, description)
        assert result.status_code in [200, 201], f"Status code: {result.status_code}"
        data = result.json()
        assert "data" in data, "Нет поля data"
        print("Keywords create работает")
    
    def test_keywords_update(self, incidents_client):
        """Тест обновления ключевого слова"""
        # Сначала получаем существующее ключевое слово
        keywords = incidents_client.get_keywords_list()
        if keywords.status_code == 200:
            data = keywords.json()
            if data.get("data") and len(data["data"]) > 0:
                keyword_id = data["data"][0].get("id")
            if keyword_id:
                result = incidents_client.update_keyword(keyword_id, description="Обновлено")
                assert result.status_code in [200, 201], f"Status code: {result.status_code}"
                print("Keywords update работает")
                return
            pytest.skip("Нет ключевых слов для обновления")
    
    def test_keywords_delete(self, incidents_client):
        """Тест удаления ключевого слова"""
        # Сначала получаем существующее ключевое слово
        keywords = incidents_client.get_keywords_list()
        if keywords.status_code == 200:
            data = keywords.json()
            if data.get("data") and len(data["data"]) > 0:
                keyword_id = data["data"][0].get("id")
            if keyword_id:
                result = incidents_client.delete_keyword(keyword_id)
                assert result.status_code in [200, 204], f"Status code: {result.status_code}"
                print("Keywords delete работает")
                return
            pytest.skip("Нет ключевых слов для удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
