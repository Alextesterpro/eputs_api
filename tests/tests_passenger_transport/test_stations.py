#!/usr/bin/env python3
"""
Тесты для Остановок (Stations) в Пассажирском транспорте
"""

import pytest
import random


class TestStations:
    """Тесты для остановок"""
    
    def test_stations_list(self, passenger_transport_client):
        """Тест получения списка остановок"""
        limit = 25
        result = passenger_transport_client.get_stations_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        stations = data.get("data", [])
        assert isinstance(stations, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(stations) <= limit, f"Количество элементов ({len(stations)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(stations) > 0:
            first_station = stations[0]
            assert "id" in first_station, "Отсутствует поле id"
            assert isinstance(first_station["id"], int), "ID должен быть числом"
            
            if "name" in first_station:
                assert isinstance(first_station["name"], str), "Name должен быть строкой"
            
            print(f"Пример остановки: ID={first_station['id']}, Name={first_station.get('name', 'N/A')}")
        
        print(f"Получено остановок: {len(stations)}")


class TestStationsCRUD:
    """CRUD тесты для остановок"""
    
    def test_station_create(self, passenger_transport_client):
        """Тест создания остановки"""
        random_int = random.randint(1000, 9999)
        name = f"Апи добавление {random_int}"
        
        # Данные для создания
        type_list = [{"id": 1, "name": "Автобус", "slug": "Bus"}]
        check_point = {
            "lat": 59.938590243283336,
            "lon": 30.335655212402347,
            "geometry": {
                "type": "Feature",
                "properties": {"radius": 10.456135836929823},
                "geometry": {"type": "Point", "coordinates": [30.33558, 59.938587]}
            }
        }
        
        result = passenger_transport_client.create_station(
            name=name,
            direction="прямо",
            comment="комментарий",
            attribute=1,
            type_list=type_list,
            view=3,
            organization_id=17,
            check_point=check_point
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Create failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true при создании"
        assert "data" in data, "Отсутствует поле data"
        
        station = data["data"]
        
        # Проверка что вернулся ID
        assert "id" in station, "Отсутствует поле id"
        station_id = station["id"]
        assert isinstance(station_id, int), "ID должен быть числом"
        assert station_id > 0, "ID должен быть положительным"
        
        # Проверка что вернулось имя
        if "name" in station:
            assert station["name"] == name, "Name не совпадает"
        
        print(f"✓ CREATE: остановка ID={station_id}, name='{name}'")
    
    def test_station_workflow(self, passenger_transport_client):
        """Workflow: CREATE -> UPDATE -> DELETE остановки"""
        
        # ===== Шаг 1: CREATE =====
        random_int = random.randint(1000, 9999)
        original_name = f"Workflow остановка {random_int}"
        
        type_list = [{"id": 1, "name": "Автобус", "slug": "Bus"}]
        check_point = {
            "lat": 59.938590243283336,
            "lon": 30.335655212402347,
            "geometry": {
                "type": "Feature",
                "properties": {"radius": 10.456135836929823},
                "geometry": {"type": "Point", "coordinates": [30.33558, 59.938587]}
            }
        }
        
        create_result = passenger_transport_client.create_station(
            name=original_name,
            direction="прямо",
            comment="тестовый комментарий",
            attribute=1,
            type_list=type_list,
            view=3,
            organization_id=17,
            check_point=check_point
        )
        
        assert create_result.status_code == 200, "Шаг 1 (CREATE) failed"
        create_data = create_result.json()
        assert create_data.get("success") is True, "Шаг 1: нет success=true"
        
        station_id = create_data["data"]["id"]
        print(f"✓ Шаг 1 (CREATE): остановка ID={station_id}, name='{original_name}'")
        
        # ===== Шаг 2: UPDATE =====
        updated_name = f"Апи редактирование {random_int}"
        
        update_result = passenger_transport_client.update_station(
            station_id=station_id,
            name=updated_name,
            direction="налево",
            comment="без комментариев",
            attribute=1,
            type_list=type_list,
            view=3,
            organization_id=4,
            check_point=check_point
        )
        
        assert update_result.status_code == 200, "Шаг 2 (UPDATE) failed"
        update_data = update_result.json()
        assert update_data.get("success") is True, "Шаг 2: нет success=true"
        
        print(f"✓ Шаг 2 (UPDATE): остановка ID={station_id} обновлена, new_name='{updated_name}'")
        
        # ===== Шаг 3: DELETE =====
        delete_result = passenger_transport_client.delete_station(station_id)
        
        assert delete_result.status_code == 200, "Шаг 3 (DELETE) failed"
        delete_data = delete_result.json()
        assert delete_data.get("success") is True, "Шаг 3: нет success=true"
        
        print(f"✓ Шаг 3 (DELETE): остановка ID={station_id} удалена")
        print(f"\n✓ Workflow завершен успешно: CREATE -> UPDATE -> DELETE")


