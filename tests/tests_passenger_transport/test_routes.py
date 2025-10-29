#!/usr/bin/env python3
"""
Тесты для Маршрутов (Routes) в Пассажирском транспорте
"""

import pytest


class TestRoutes:
    """Тесты для маршрутов"""
    
    def test_routes_list(self, passenger_transport_client):
        """Тест получения списка маршрутов"""
        limit = 25
        result = passenger_transport_client.get_routes_list(page=1, limit=limit, status_list=[1, 2])
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        routes = data.get("data", [])
        assert isinstance(routes, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(routes) <= limit, f"Количество элементов ({len(routes)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(routes) > 0:
            first_route = routes[0]
            assert "id" in first_route or "name" in first_route or "num" in first_route, "Отсутствуют ключевые поля"
            
            if "id" in first_route:
                assert isinstance(first_route["id"], int), "ID должен быть числом"
            if "name" in first_route:
                assert isinstance(first_route["name"], str), "Name должен быть строкой"
            
            print(f"Пример маршрута: {first_route}")
        
        print(f"Получено маршрутов: {len(routes)}")
    
    def test_trans_organizations_list(self, passenger_transport_client):
        """Тест получения списка привязки организаций"""
        limit = 25
        result = passenger_transport_client.get_trans_organizations_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        orgs = data.get("data", [])
        assert isinstance(orgs, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(orgs) <= limit, f"Количество элементов ({len(orgs)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(orgs) > 0:
            first_org = orgs[0]
            if "id" in first_org:
                assert isinstance(first_org["id"], int), "ID должен быть числом"
            if "title" in first_org:
                assert isinstance(first_org["title"], str), "Title должен быть строкой"
            
            print(f"Пример организации: {first_org}")
        
        print(f"Получено организаций: {len(orgs)}")


