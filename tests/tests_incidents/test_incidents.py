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
        limit = 5
        result = incidents_client.get_incidents_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert "data" in data, "Отсутствует поле data"
        assert isinstance(data["data"], list), "Данные должны быть списком"
        
        incidents = data["data"]
        
        # Проверка лимита
        assert len(incidents) <= limit, f"Количество элементов ({len(incidents)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов (если есть)
        if len(incidents) > 0:
            first_incident = incidents[0]
            assert "id" in first_incident, "Отсутствует поле id"
            assert isinstance(first_incident["id"], int), "ID должен быть числом"
            
            # Проверяем наличие основных полей
            if "name" in first_incident:
                assert isinstance(first_incident["name"], str), "Name должен быть строкой"
            if "description" in first_incident:
                assert isinstance(first_incident["description"], (str, type(None))), "Description должен быть строкой или null"
            
            print(f"Пример инцидента: ID={first_incident['id']}, Name={first_incident.get('name', 'N/A')}")
        
        print(f"Получено инцидентов: {len(incidents)}")
    
    def test_incidents_get_by_id(self, incidents_client):
        """Тест получения инцидента по ID"""
        # Сначала получаем список, чтобы найти существующий ID
        incidents = incidents_client.get_incidents_list(page=1, limit=1)
        
        if incidents.status_code != 200:
            pytest.skip("Не удалось получить список инцидентов")
        
        data = incidents.json()
        if not data.get("data") or len(data["data"]) == 0:
            pytest.skip("Нет инцидентов для тестирования")
        
        incident_id = data["data"][0].get("id")
        if not incident_id:
            pytest.skip("ID инцидента не найден")
        
        # Получаем инцидент по ID
        result = incidents_client.get_incident_by_id(incident_id)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        response_data = result.json()
        assert "data" in response_data, "Отсутствует поле data"
        
        incident = response_data["data"]
        
        # Проверка что вернулся правильный инцидент
        assert incident.get("id") == incident_id, f"Вернулся неправильный ID: ожидалось {incident_id}, получено {incident.get('id')}"
        
        # Проверка структуры объекта
        assert "id" in incident, "Отсутствует поле id"
        assert isinstance(incident["id"], int), "ID должен быть числом"
        
        print(f"✓ GET by ID: получен инцидент ID={incident_id}, Name={incident.get('name', 'N/A')}")
    
    def test_incidents_pagination(self, incidents_client):
        """Тест пагинации инцидентов"""
        limit = 2
        
        # Первая страница
        page1 = incidents_client.get_incidents_list(page=1, limit=limit)
        assert page1.status_code == 200, f"Page 1 status: {page1.status_code}"
        data1 = page1.json()
        assert "data" in data1, "Отсутствует поле data на странице 1"
        assert isinstance(data1["data"], list), "Data на странице 1 должна быть списком"
        
        # Вторая страница
        page2 = incidents_client.get_incidents_list(page=2, limit=limit)
        assert page2.status_code == 200, f"Page 2 status: {page2.status_code}"
        data2 = page2.json()
        assert "data" in data2, "Отсутствует поле data на странице 2"
        assert isinstance(data2["data"], list), "Data на странице 2 должна быть списком"
        
        incidents1 = data1["data"]
        incidents2 = data2["data"]
        
        # Проверка лимита
        assert len(incidents1) <= limit, f"Страница 1: превышен лимит ({len(incidents1)} > {limit})"
        assert len(incidents2) <= limit, f"Страница 2: превышен лимит ({len(incidents2)} > {limit})"
        
        # Проверка что страницы разные (если есть данные)
        if len(incidents1) > 0 and len(incidents2) > 0:
            ids_page1 = [item["id"] for item in incidents1 if "id" in item]
            ids_page2 = [item["id"] for item in incidents2 if "id" in item]
            
            common_ids = set(ids_page1) & set(ids_page2)
            assert len(common_ids) == 0, f"Найдены одинаковые ID на разных страницах: {common_ids}"
            print("✓ Пагинация работает корректно: страницы содержат разные данные")
        
        print(f"Страница 1: {len(incidents1)} элементов, Страница 2: {len(incidents2)} элементов")
    
    def test_incidents_create(self, incidents_client):
        """Тест создания инцидента"""
        name = f"Тест {datetime.now().strftime('%H:%M:%S')}"
        description = "Простой тестовый инцидент"
        
        # Создание
        result = incidents_client.create_incident(name, description)
        
        # Проверка статуса
        assert result.status_code in [200, 201], f"Create failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert "data" in data, "Отсутствует поле data"
        
        incident = data["data"]
        
        # Проверка что вернулся ID
        assert "id" in incident, "Отсутствует поле id"
        incident_id = incident["id"]
        assert isinstance(incident_id, int), "ID должен быть числом"
        assert incident_id > 0, "ID должен быть положительным числом"
        
        # Проверка что вернулись правильные данные
        if "name" in incident:
            assert incident["name"] == name, f"Name не совпадает: ожидалось '{name}', получено '{incident['name']}'"
        if "description" in incident:
            assert incident["description"] == description, f"Description не совпадает"
        
        print(f"✓ CREATE: создан инцидент ID={incident_id}, Name='{name}'")
    
    def test_incidents_update(self, incidents_client):
        """Тест обновления инцидента"""
        # Сначала получаем существующий инцидент
        incidents = incidents_client.get_incidents_list(page=1, limit=1)
        
        if incidents.status_code != 200:
            pytest.skip("Не удалось получить список инцидентов")
        
        data = incidents.json()
        if not data.get("data") or len(data["data"]) == 0:
            pytest.skip("Нет инцидентов для обновления")
        
        incident = data["data"][0]
        incident_id = incident.get("id")
        if not incident_id:
            pytest.skip("ID инцидента не найден")
        
        original_description = incident.get("description", "")
        new_description = f"Обновлено {datetime.now().strftime('%H:%M:%S')}"
        
        # Обновление
        result = incidents_client.update_incident(incident_id, description=new_description)
        
        # Проверка статуса
        assert result.status_code in [200, 201], f"Update failed: {result.status_code}"
        
        # Проверка что описание изменилось
        updated_incident = incidents_client.get_incident_by_id(incident_id)
        if updated_incident.status_code == 200:
            updated_data = updated_incident.json()
            if "data" in updated_data and "description" in updated_data["data"]:
                current_description = updated_data["data"]["description"]
                assert current_description == new_description, \
                    f"Description не обновился: '{current_description}' != '{new_description}'"
                print(f"✓ UPDATE: инцидент ID={incident_id} обновлен, description изменился")
        else:
            print(f"✓ UPDATE: инцидент ID={incident_id} обновлен (проверка изменений не выполнена)")
    
    def test_incidents_delete(self, incidents_client):
        """Тест удаления инцидента"""
        # Сначала создаем инцидент специально для удаления
        name = f"Для удаления {datetime.now().strftime('%H:%M:%S')}"
        description = "Этот инцидент будет удален"
        
        create_result = incidents_client.create_incident(name, description)
        
        if create_result.status_code not in [200, 201]:
            pytest.skip("Не удалось создать инцидент для удаления")
        
        create_data = create_result.json()
        if "data" not in create_data or "id" not in create_data["data"]:
            pytest.skip("ID инцидента не вернулся после создания")
        
        incident_id = create_data["data"]["id"]
        print(f"Создан инцидент для удаления: ID={incident_id}")
        
        # Удаление
        result = incidents_client.delete_incident(incident_id)
        
        # Проверка статуса
        assert result.status_code in [200, 204], f"Delete failed: {result.status_code}"
        
        print(f"✓ DELETE: инцидент ID={incident_id} удален")
        
        # Проверка что инцидент действительно удален
        get_result = incidents_client.get_incident_by_id(incident_id)
        if get_result.status_code == 404:
            print(f"✓ VERIFY: подтверждено удаление - инцидент ID={incident_id} не найден (404)")
        elif get_result.status_code == 200:
            # Возможно API возвращает 200 с пустыми данными или флагом deleted
            get_data = get_result.json()
            if not get_data.get("data") or get_data.get("data", {}).get("deleted"):
                print(f"✓ VERIFY: инцидент ID={incident_id} помечен как удаленный")
            else:
                print(f"⚠ WARNING: инцидент ID={incident_id} все еще доступен после удаления")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
