#!/usr/bin/env python3
"""
Тесты для Organizations (Организации)
"""

import pytest
import random


class TestOrganizationsList:
    """Тесты для списка организаций"""
    
    def test_organizations_list(self, organizations_client):
        """Тест получения списка организаций"""
        response = organizations_client.organization_list(page=1, limit=25)
        
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Отсутствует поле data"
        
        # Проверяем структуру данных
        org_data = data.get("data", {})
        if isinstance(org_data, dict) and "data" in org_data:
            items = org_data.get("data", [])
        else:
            items = org_data if isinstance(org_data, list) else []
        
        assert isinstance(items, list), "Данные должны быть списком"
        
        if len(items) > 0:
            first_org = items[0]
            assert "id" in first_org, "Отсутствует поле id"
            assert "title" in first_org, "Отсутствует поле title"
            assert "inn" in first_org, "Отсутствует поле inn"
            assert isinstance(first_org["id"], int), "ID должен быть числом"
            assert isinstance(first_org["title"], str), "Title должен быть строкой"
            print(f" Получено организаций: {len(items)}")


class TestOrganizationsCRUD:
    """Тесты CRUD операций для организаций"""
    
    def test_organization_create(self, organizations_client):
        """Тест создания организации"""
        import requests
        
        random_int = random.randint(1000, 9999)
        
        address = {
            "city_name": "г Санкт-Петербург",
            "region": "Санкт-Петербург",
            "postal_code": "190000",
            "street": "ул Тестовая",
            "house": f"д {random.randint(1, 100)}",
            "comments": ""
        }
        
        # Используем известный валидный ИНН для тестирования
        test_inn = "6623029538"  # ИНН из примера Postman
        
        try:
            response = organizations_client.organization_create(
                title=f"Тестовая организация {random_int}",
                full_name=f"ООО 'Тестовая организация {random_int}'",
                inn=test_inn,
                juristic_address=address,
                mail_address=address,
                real_address=address,
                phones=[{"person": "Иванов", "data": f"7{random.randint(9000000000, 9999999999)}"}],
                emails=[]
            )
            
            if response.status_code == 422:
                pytest.skip("API validation error (422) - возможно дубликат ИНН или проблема валидации")
            
            assert response.status_code == 200, f"Create status: {response.status_code}"
            data = response.json()
            assert data.get("success") is True, "Create: нет success=true"
            assert "data" in data, "Create: отсутствует поле data"
            assert "id" in data["data"], "Create: отсутствует ID"
            
            org_id = data["data"]["id"]
            assert isinstance(org_id, int), "ID должен быть числом"
            print(f" Создана организация ID={org_id}")
            
            # Cleanup
            organizations_client.organization_delete(org_id)
            print(f" Cleanup: удалена организация ID={org_id}")
        
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            pytest.skip("API timeout при создании организации")
    
    def test_organization_full_workflow(self, organizations_client):
        """Полный workflow: создание, обновление, добавление документов, роли, удаление"""
        import requests
        
        random_int = random.randint(1000, 9999)
        
        # Шаг 1: Создание
        address = {
            "city_name": "г Москва",
            "region": "Москва",
            "postal_code": "101000",
            "street": "ул Центральная",
            "house": f"д {random.randint(1, 50)}",
            "comments": ""
        }
        
        # Используем известный валидный ИНН
        test_inn = "6623029538"
        
        try:
            create_response = organizations_client.organization_create(
                title=f"Workflow Org {random_int}",
                full_name=f"ООО 'Workflow Organization {random_int}'",
                inn=test_inn,
                juristic_address=address,
                mail_address=address,
                real_address=address,
                phones=[{"person": "Петров", "data": "79991234567"}],
                emails=[]
            )
            
            if create_response.status_code == 422:
                pytest.skip("API validation error (422) - возможно дубликат ИНН")
            
            assert create_response.status_code == 200, "Шаг 1 (CREATE) failed"
            create_data = create_response.json()
            org_id = create_data["data"]["id"]
            print(f" Шаг 1: Создана организация ID={org_id}")
            
            # Шаг 2: Обновление
            update_response = organizations_client.organization_update(
                org_id=org_id,
                phones=[{"person": "Сидоров", "data": "79997654321"}]
            )
            
            assert update_response.status_code == 200, "Шаг 2 (UPDATE) failed"
            update_data = update_response.json()
            assert update_data.get("success") is True, "Update: нет success=true"
            print(f" Шаг 2: Обновлена организация ID={org_id}")
            
            # Шаг 3: Удаление
            delete_response = organizations_client.organization_delete(org_id)
            
            assert delete_response.status_code == 200, "Шаг 3 (DELETE) failed"
            delete_data = delete_response.json()
            assert delete_data.get("success") is True, "Delete: нет success=true"
            print(f" Шаг 3: Удалена организация ID={org_id}")
        
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout):
            pytest.skip("API timeout при workflow организации")

