#!/usr/bin/env python3
"""
Тесты для раздела Парковочное пространство
"""

import pytest
import random


class TestParking:
    """Базовые тесты для парковок"""
    
    def test_parking_list(self, parking_client):
        """Тест получения списка парковок"""
        limit = 25
        result = parking_client.get_parking_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        parkings = data.get("data", [])
        assert isinstance(parkings, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(parkings) <= limit, f"Количество элементов ({len(parkings)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(parkings) > 0:
            first_parking = parkings[0]
            assert "id" in first_parking, "Отсутствует поле id"
            assert isinstance(first_parking["id"], int), "ID должен быть числом"
            
            if "name" in first_parking:
                assert isinstance(first_parking["name"], str), "Name должен быть строкой"
            if "lat" in first_parking and "lon" in first_parking:
                # API может возвращать координаты как строки или числа
                lat_val = first_parking["lat"]
                lon_val = first_parking["lon"]
                if isinstance(lat_val, str):
                    lat_val = float(lat_val)
                if isinstance(lon_val, str):
                    lon_val = float(lon_val)
                assert isinstance(lat_val, (int, float)), "Latitude должен быть числом"
                assert isinstance(lon_val, (int, float)), "Longitude должен быть числом"
            
            print(f"Пример парковки: ID={first_parking['id']}, Name={first_parking.get('name', 'N/A')}")
        
        print(f"Получено парковок: {len(parkings)}")
    
    def test_parking_pagination(self, parking_client):
        """Тест пагинации списка парковок"""
        limit = 5
        
        # Первая страница
        result_page1 = parking_client.get_parking_list(page=1, limit=limit)
        assert result_page1.status_code == 200, f"Page 1 status: {result_page1.status_code}"
        
        data1 = result_page1.json()
        assert data1.get("success") is True, "Page 1: нет success=true"
        assert "data" in data1, "Page 1: нет поля data"
        
        parkings1 = data1["data"]
        assert len(parkings1) <= limit, f"Page 1: превышен лимит ({len(parkings1)} > {limit})"
        
        # Вторая страница
        result_page2 = parking_client.get_parking_list(page=2, limit=limit)
        assert result_page2.status_code == 200, f"Page 2 status: {result_page2.status_code}"
        
        data2 = result_page2.json()
        assert data2.get("success") is True, "Page 2: нет success=true"
        
        parkings2 = data2["data"]
        assert len(parkings2) <= limit, f"Page 2: превышен лимит ({len(parkings2)} > {limit})"
        
        # Проверка что страницы разные
        if len(parkings1) > 0 and len(parkings2) > 0:
            ids1 = [p["id"] for p in parkings1 if "id" in p]
            ids2 = [p["id"] for p in parkings2 if "id" in p]
            
            common_ids = set(ids1) & set(ids2)
            assert len(common_ids) == 0, f"Найдены одинаковые ID на разных страницах: {common_ids}"
            print(" Пагинация: страницы содержат разные данные")
        
        print(f"Страница 1: {len(parkings1)}, Страница 2: {len(parkings2)}")


class TestParkingCRUD:
    """CRUD тесты для парковок"""
    
    def test_parking_create(self, parking_client):
        """Тест создания парковки"""
        random_int = random.randint(1000, 9999)
        name = f"Апи добавление {random_int}"
        address = parking_client.generate_test_address()
        address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая площадь, 4"
        lat = 59.943716
        lon = 30.305395
        
        # Создание
        result = parking_client.create_parking(
            name=name,
            address=address,
            address_text=address_text,
            contacts="1234567",
            description="описание",
            lat=lat,
            lon=lon,
            tariff_id=23,
            category_id=35,
            is_aggregating=True,
            is_blocked=True,
            total="2",
            common="2",
            handicapped="2"
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Create failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true при создании"
        assert "data" in data, "Отсутствует поле data"
        
        parking = data["data"]
        
        # Проверка что вернулся ID
        assert "id" in parking, "Отсутствует поле id"
        parking_id = parking["id"]
        assert isinstance(parking_id, int), "ID должен быть числом"
        assert parking_id > 0, "ID должен быть положительным"
        
        # Проверка что вернулись правильные данные
        if "name" in parking:
            assert parking["name"] == name, f"Name не совпадает"
        if "lat" in parking:
            assert abs(parking["lat"] - lat) < 0.0001, "Latitude не совпадает"
        if "lon" in parking:
            assert abs(parking["lon"] - lon) < 0.0001, "Longitude не совпадает"
        
        print(f" CREATE: парковка ID={parking_id}, name='{name}'")
    
    def test_parking_update(self, parking_client):
        """Тест обновления парковки"""
        # Создаем парковку
        random_int = random.randint(1000, 9999)
        original_name = f"Апи для обновления {random_int}"
        address = parking_client.generate_test_address()
        address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая площадь, 4"
        
        create_result = parking_client.create_parking(
            name=original_name,
            address=address,
            address_text=address_text,
            contacts="1234567",
            description="описание",
            lat=59.943716,
            lon=30.305395
        )
        
        assert create_result.status_code == 200, "Create failed"
        create_data = create_result.json()
        parking_id = create_data["data"]["id"]
        print(f"Создана парковка для обновления: ID={parking_id}")
        
        # Обновляем
        updated_name = "Апи редактирование"
        updated_contacts = "987638495"
        updated_address = {**address, "house": "1/1", "street": "Биржевая линия"}
        updated_address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая линия, 1/1"
        
        update_data = {
            "name": updated_name,
            "address": updated_address,
            "address_text": updated_address_text,
            "contacts": updated_contacts,
            "description": "новое описание",
            "location": {
                "type": "Feature",
                "properties": {"radius": 33.00792661617949},
                "geometry": {"type": "Point", "coordinates": [30.305271, 59.943751]}
            },
            "tariff_id": 20,
            "category_id": 35,
            "photo": "http://91.227.17.139/services/storage//api/document/public/81379bcc85ca84c8e169060223a658e2",
            "is_aggregating": False,
            "is_blocked": False,
            "total": "6",
            "common": "5",
            "handicapped": "6",
            "lat": 59.94384159808314,
            "lon": 30.296649863392695,
            "spaces": {"common": "5", "total": "6", "handicapped": "6"}
        }
        
        update_result = parking_client.update_parking(parking_id, **update_data)
        
        # Проверка статуса
        assert update_result.status_code == 200, f"Update failed: {update_result.status_code}"
        
        # Проверка структуры ответа
        update_response = update_result.json()
        assert update_response.get("success") is True, "Отсутствует success=true при обновлении"
        
        # Проверка что данные изменились
        if "data" in update_response:
            updated_parking = update_response["data"]
            if "name" in updated_parking:
                assert updated_parking["name"] == updated_name, "Name не обновился"
                assert updated_parking["name"] != original_name, "Name не изменился"
        
        print(f" UPDATE: парковка ID={parking_id} обновлена, name='{updated_name}'")
    
    def test_parking_delete(self, parking_client):
        """Тест удаления парковки"""
        # Создаем парковку
        random_int = random.randint(1000, 9999)
        name = f"Апи для удаления {random_int}"
        address = parking_client.generate_test_address()
        address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая площадь, 4"
        
        create_result = parking_client.create_parking(
            name=name,
            address=address,
            address_text=address_text,
            contacts="1234567",
            description="описание",
            lat=59.943716,
            lon=30.305395
        )
        
        assert create_result.status_code == 200, "Create failed"
        create_data = create_result.json()
        parking_id = create_data["data"]["id"]
        print(f"Создана парковка для удаления: ID={parking_id}")
        
        # Удаляем
        delete_result = parking_client.delete_parking(parking_id)
        
        # Проверка статуса
        assert delete_result.status_code == 200, f"Delete failed: {delete_result.status_code}"
        
        # Проверка структуры ответа
        delete_data = delete_result.json()
        assert delete_data.get("success") is True, "Отсутствует success=true при удалении"
        
        print(f" DELETE: парковка ID={parking_id} удалена")


class TestParkingWorkflow:
    """Workflow тесты для парковок"""
    
    def test_parking_full_workflow(self, parking_client):
        """Полный workflow: CREATE -> UPDATE -> VERIFY -> DELETE"""
        
        # ===== Шаг 1: CREATE =====
        random_int = random.randint(1000, 9999)
        name = f"Workflow парковка {random_int}"
        address = parking_client.generate_test_address()
        address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая площадь, 4"
        
        create_result = parking_client.create_parking(
            name=name,
            address=address,
            address_text=address_text,
            contacts="1234567",
            description="тестовое описание",
            lat=59.943716,
            lon=30.305395,
            total="3",
            common="2",
            handicapped="1"
        )
        
        assert create_result.status_code == 200, "Шаг 1 (CREATE) failed"
        create_data = create_result.json()
        assert create_data.get("success") is True, "Шаг 1: нет success=true"
        
        parking_id = create_data["data"]["id"]
        print(f" Шаг 1 (CREATE): парковка ID={parking_id}, name='{name}'")
        
        # ===== Шаг 2: UPDATE =====
        updated_name = f"Обновленная парковка {random_int}"
        update_data = {
            "name": updated_name,
            "address": address,
            "address_text": address_text,
            "contacts": "9999999",
            "description": "обновленное описание",
            "location": {
                "type": "Feature",
                "properties": {"radius": 20},
                "geometry": {"type": "Point", "coordinates": [30.305395, 59.943716]}
            },
            "tariff_id": 23,
            "category_id": 35,
            "photo": "http://91.227.17.139/services/storage//api/document/public/81379bcc85ca84c8e169060223a658e2",
            "is_aggregating": False,
            "is_blocked": False,
            "total": "5",
            "common": "4",
            "handicapped": "1",
            "lat": 59.943716,
            "lon": 30.305395,
            "spaces": {"common": "4", "total": "5", "handicapped": "1"}
        }
        
        update_result = parking_client.update_parking(parking_id, **update_data)
        assert update_result.status_code == 200, "Шаг 2 (UPDATE) failed"
        assert update_result.json().get("success") is True, "Шаг 2: нет success=true"
        
        print(f" Шаг 2 (UPDATE): парковка ID={parking_id} обновлена, new_name='{updated_name}'")
        
        # ===== Шаг 3: VERIFY в списке =====
        list_result = parking_client.get_parking_list(page=1, limit=100)
        assert list_result.status_code == 200, "Шаг 3 (VERIFY) failed"
        
        list_data = list_result.json()
        parkings = list_data.get("data", [])
        parking_exists = any(p.get("id") == parking_id for p in parkings)
        
        assert parking_exists, f"Шаг 3: парковка ID={parking_id} не найдена в списке"
        print(f" Шаг 3 (VERIFY): парковка ID={parking_id} найдена в списке")
        
        # ===== Шаг 4: DELETE =====
        delete_result = parking_client.delete_parking(parking_id)
        assert delete_result.status_code == 200, "Шаг 4 (DELETE) failed"
        assert delete_result.json().get("success") is True, "Шаг 4: нет success=true"
        
        print(f" Шаг 4 (DELETE): парковка ID={parking_id} удалена")
        
        # ===== Итог =====
        print(f"\n Workflow завершен успешно: CREATE -> UPDATE -> VERIFY -> DELETE")

