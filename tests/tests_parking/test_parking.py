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
        result = parking_client.get_parking_list(page=1, limit=25)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Нет поля data в ответе"
        print(f"Parking list: найдено {len(data.get('data', []))} парковок")
    
    def test_parking_pagination(self, parking_client):
        """Тест пагинации списка парковок"""
        result = parking_client.get_parking_list(page=1, limit=5)
        assert result.status_code == 200
        data = result.json()
        assert data.get("success") is True
        assert "data" in data
        print(f"Pagination test: получено {len(data.get('data', []))} записей (limit=5)")


class TestParkingCRUD:
    """CRUD тесты для парковок"""
    
    def test_parking_create(self, parking_client):
        """Тест создания парковки"""
        random_int = random.randint(1000, 9999)
        name = f"Апи добавление {random_int}"
        address = parking_client.generate_test_address()
        address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая площадь, 4"
        
        result = parking_client.create_parking(
            name=name,
            address=address,
            address_text=address_text,
            contacts="1234567",
            description="описание",
            lat=59.943716,
            lon=30.305395,
            tariff_id=23,
            category_id=35,
            is_aggregating=True,
            is_blocked=True,
            total="2",
            common="2",
            handicapped="2"
        )
        
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Создание не прошло"
        assert "data" in data, "Нет данных о созданной парковке"
        assert "id" in data["data"], "Нет ID созданной парковки"
        print(f"Создана парковка с ID: {data['data']['id']}")
    
    def test_parking_update(self, parking_client):
        """Тест обновления парковки"""
        # Сначала создаем парковку
        random_int = random.randint(1000, 9999)
        name = f"Апи для обновления {random_int}"
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
        
        assert create_result.status_code == 200
        create_data = create_result.json()
        parking_id = create_data["data"]["id"]
        
        # Теперь обновляем
        updated_address = {
            **address,
            "house": "1/1",
            "street": "Биржевая линия"
        }
        updated_address_text = "Санкт-Петербург, Санкт-Петербург, Василеостровский район, Биржевая линия, 1/1"
        
        update_data = {
            "name": "Апи редактирование",
            "address": updated_address,
            "address_text": updated_address_text,
            "contacts": "987638495",
            "description": "новое описание",
            "location": {
                "type": "Feature",
                "properties": {
                    "radius": 33.00792661617949
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [30.305271, 59.943751]
                }
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
            "spaces": {
                "common": "5",
                "total": "6",
                "handicapped": "6"
            }
        }
        
        update_result = parking_client.update_parking(parking_id, **update_data)
        assert update_result.status_code == 200, f"Обновление не прошло: {update_result.status_code}"
        update_response = update_result.json()
        assert update_response.get("success") is True, "Обновление не прошло"
        print(f"Парковка {parking_id} обновлена")
    
    def test_parking_delete(self, parking_client):
        """Тест удаления парковки"""
        # Сначала создаем парковку
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
        
        assert create_result.status_code == 200
        create_data = create_result.json()
        parking_id = create_data["data"]["id"]
        
        # Теперь удаляем
        delete_result = parking_client.delete_parking(parking_id)
        assert delete_result.status_code == 200, f"Удаление не прошло: {delete_result.status_code}"
        delete_data = delete_result.json()
        assert delete_data.get("success") is True, "Удаление не прошло"
        print(f"Парковка {parking_id} удалена")


class TestParkingWorkflow:
    """Workflow тесты для парковок"""
    
    def test_parking_full_workflow(self, parking_client):
        """Полный цикл: создание -> обновление -> удаление парковки"""
        # 1. Создание
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
        
        assert create_result.status_code == 200, "Создание не прошло"
        create_data = create_result.json()
        assert create_data.get("success") is True
        parking_id = create_data["data"]["id"]
        print(f"1. Создана парковка ID: {parking_id}")
        
        # 2. Обновление
        update_data = {
            "name": f"Обновленная парковка {random_int}",
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
        assert update_result.status_code == 200, "Обновление не прошло"
        assert update_result.json().get("success") is True
        print(f"2. Парковка {parking_id} обновлена")
        
        # 3. Проверка в списке
        list_result = parking_client.get_parking_list(page=1, limit=100)
        assert list_result.status_code == 200
        list_data = list_result.json()
        parking_exists = any(p.get("id") == parking_id for p in list_data.get("data", []))
        assert parking_exists, f"Парковка {parking_id} не найдена в списке"
        print(f"3. Парковка {parking_id} найдена в списке")
        
        # 4. Удаление
        delete_result = parking_client.delete_parking(parking_id)
        assert delete_result.status_code == 200, "Удаление не прошло"
        assert delete_result.json().get("success") is True
        print(f"4. Парковка {parking_id} удалена")
        
        print("Workflow парковки выполнен успешно")

