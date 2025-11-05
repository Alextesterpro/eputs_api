#!/usr/bin/env python3
"""
Тесты для Roles (Роли организаций)
"""

import pytest
import random


class TestRolesList:
    """Тесты для списка ролей"""
    
    def test_roles_list(self, organizations_client):
        """Тест получения списка ролей организаций"""
        response = organizations_client.role_list(page=1, limit=25)
        
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Отсутствует поле data"
        
        # Проверяем структуру данных
        role_data = data.get("data", {})
        if isinstance(role_data, dict) and "data" in role_data:
            items = role_data.get("data", [])
        else:
            items = role_data if isinstance(role_data, list) else []
        
        assert isinstance(items, list), "Данные должны быть списком"
        
        if len(items) > 0:
            first_role = items[0]
            assert "id" in first_role, "Отсутствует поле id"
            assert "name" in first_role, "Отсутствует поле name"
            assert isinstance(first_role["id"], int), "ID должен быть числом"
            assert isinstance(first_role["name"], str), "Name должен быть строкой"
            print(f"✓ Получено ролей: {len(items)}")


class TestRolesCRUD:
    """Тесты CRUD операций для ролей"""
    
    def test_role_workflow(self, organizations_client):
        """Полный workflow: создание, редактирование, удаление роли"""
        random_int = random.randint(1000, 9999)
        
        # Создание
        create_name = f"Апи добавление {random_int}"
        create_response = organizations_client.role_create(name=create_name)
        
        assert create_response.status_code == 200, f"Create status: {create_response.status_code}"
        create_data = create_response.json()
        assert create_data.get("success") is True, "Create: нет success=true"
        assert "data" in create_data, "Create: отсутствует поле data"
        assert "id" in create_data["data"], "Create: отсутствует ID"
        
        role_id = create_data["data"]["id"]
        assert isinstance(role_id, int), "ID должен быть числом"
        print(f"✓ Создана роль ID={role_id}, name='{create_name}'")
        
        # Редактирование
        update_name = f"Апи редактирование {random.randint(1000, 9999)}"
        update_response = organizations_client.role_update(role_id=role_id, name=update_name)
        
        assert update_response.status_code == 200, f"Update status: {update_response.status_code}"
        update_data = update_response.json()
        assert update_data.get("success") is True, "Update: нет success=true"
        print(f"✓ Обновлена роль ID={role_id}, new_name='{update_name}'")
        
        # Удаление
        delete_response = organizations_client.role_delete(role_id=role_id)
        
        assert delete_response.status_code == 200, f"Delete status: {delete_response.status_code}"
        delete_data = delete_response.json()
        assert delete_data.get("success") is True, "Delete: нет success=true"
        print(f"✓ Удалена роль ID={role_id}")

