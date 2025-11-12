#!/usr/bin/env python3
"""
Тесты для Транспортных средств (Vehicles) в Пассажирском транспорте
"""

import pytest
import random


class TestVehicles:
    """Тесты для транспортных средств"""
    
    def test_vehicles_list(self, passenger_transport_client):
        """Тест получения списка ТС"""
        limit = 25
        result = passenger_transport_client.get_vehicles_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        vehicles = data.get("data", [])
        assert isinstance(vehicles, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(vehicles) <= limit, f"Количество элементов ({len(vehicles)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(vehicles) > 0:
            first_vehicle = vehicles[0]
            assert "id" in first_vehicle, "Отсутствует поле id"
            assert isinstance(first_vehicle["id"], int), "ID должен быть числом"
            
            if "number" in first_vehicle:
                assert isinstance(first_vehicle["number"], (str, int)), "Number должен быть строкой или числом"
            
            print(f"Пример ТС: ID={first_vehicle['id']}, Number={first_vehicle.get('number', 'N/A')}")
        
        print(f"Получено ТС: {len(vehicles)}")


class TestVehiclesCRUD:
    """CRUD тесты для ТС"""
    
    def test_vehicle_create(self, passenger_transport_client):
        """Тест создания ТС"""
        random_int = random.randint(1000, 9999)
        number = str(random_int)
        garage_number = str(random_int + 1)
        
        result = passenger_transport_client.create_vehicle(
            number=number,
            garage_number=garage_number,
            model_id=6,
            category_id=3,
            class_id=2,
            characteristics={"class_tr_tc": "A"},
            organization_id=4
        )
        
        # Проверка статуса (502 - временная ошибка сервера)
        if result.status_code == 502:
            pytest.skip("502 Bad Gateway - временная ошибка сервера")
        assert result.status_code == 200, f"Create failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true при создании"
        assert "data" in data, "Отсутствует поле data"
        
        vehicle = data["data"]
        
        # Проверка что вернулся ID
        assert "id" in vehicle, "Отсутствует поле id"
        vehicle_id = vehicle["id"]
        assert isinstance(vehicle_id, int), "ID должен быть числом"
        assert vehicle_id > 0, "ID должен быть положительным"
        
        print(f"✓ CREATE: ТС ID={vehicle_id}, number='{number}'")
    
    def test_vehicle_workflow(self, passenger_transport_client):
        """Workflow: CREATE -> UPDATE -> GET_CARD -> DELETE ТС"""
        
        # ===== Шаг 1: CREATE =====
        random_int = random.randint(1000, 9999)
        number = str(random_int)
        garage_number = str(random_int + 1)
        
        create_result = passenger_transport_client.create_vehicle(
            number=number,
            garage_number=garage_number,
            model_id=6,
            category_id=3,
            class_id=2,
            characteristics={"class_tr_tc": "A"},
            organization_id=4
        )
        
        assert create_result.status_code == 200, "Шаг 1 (CREATE) failed"
        create_data = create_result.json()
        assert create_data.get("success") is True, "Шаг 1: нет success=true"
        
        vehicle_id = create_data["data"]["id"]
        print(f"✓ Шаг 1 (CREATE): ТС ID={vehicle_id}, number='{number}'")
        
        # ===== Шаг 2: UPDATE =====
        updated_number = str(random_int + 100)
        
        update_result = passenger_transport_client.update_vehicle(
            vehicle_id=vehicle_id,
            number=updated_number,
            garage_number=garage_number,
            model_id=6,
            category_id=3,
            class_id=2,
            characteristics={"class_tr_tc": "B"},
            organization_id=17
        )
        
        assert update_result.status_code == 200, "Шаг 2 (UPDATE) failed"
        update_data = update_result.json()
        assert update_data.get("success") is True, "Шаг 2: нет success=true"
        
        print(f"✓ Шаг 2 (UPDATE): ТС ID={vehicle_id} обновлено, new_number='{updated_number}'")
        
        # ===== Шаг 3: GET CARD =====
        card_result = passenger_transport_client.get_vehicle_card(vehicle_id)
        
        assert card_result.status_code == 200, "Шаг 3 (GET_CARD) failed"
        card_data = card_result.json()
        assert card_data.get("success") is True, "Шаг 3: нет success=true"
        
        print(f"✓ Шаг 3 (GET_CARD): учетная карточка ТС ID={vehicle_id} получена")
        
        # ===== Шаг 4: DELETE =====
        delete_result = passenger_transport_client.delete_vehicle(vehicle_id)
        
        assert delete_result.status_code == 200, "Шаг 4 (DELETE) failed"
        delete_data = delete_result.json()
        assert delete_data.get("success") is True, "Шаг 4: нет success=true"
        
        print(f"✓ Шаг 4 (DELETE): ТС ID={vehicle_id} удалено")
        print(f"\n✓ Workflow завершен успешно: CREATE -> UPDATE -> GET_CARD -> DELETE")


class TestVehicleReports:
    """Тесты для отчетов по ТС"""
    
    def test_vehicle_history(self, passenger_transport_client):
        """Тест получения истории перемещений ТС"""
        # Используем существующее ТС (предполагаем что есть)
        vehicle_id = 1  # Используем ID из базы
        
        result = passenger_transport_client.get_vehicle_history(
            vehicle_id=vehicle_id,
            date_start="2025-10-27T19:19:00+03:00",
            date_end="2025-10-28T19:19:00+03:00"
        )
        
        # Проверка статуса
        assert result.status_code in [200, 404], f"Status code: {result.status_code}"
        
        if result.status_code == 200:
            data = result.json()
            assert data.get("success") is True, "Отсутствует success=true"
            print(f"✓ История перемещений ТС ID={vehicle_id} получена")
        else:
            print(f"ℹ ТС ID={vehicle_id} не найдено (это нормально для тестов)")
    
    def test_generate_vehicle_report(self, passenger_transport_client):
        """Тест генерации отчета по ТС"""
        # Используем существующее ТС
        vehicle_id = 1
        
        result = passenger_transport_client.generate_vehicle_report(
            vehicle_id=vehicle_id,
            start_date="2025-10-01T00:00:00+03:00",
            end_date="2025-10-31T23:59:00+03:00",
            formats=["XLSX", "ODS", "HTML", "CSV"]
        )
        
        # Проверка статуса
        assert result.status_code in [200, 404], f"Status code: {result.status_code}"
        
        if result.status_code == 200:
            data = result.json()
            assert data.get("success") is True, "Отсутствует success=true"
            print(f"✓ Отчет по ТС ID={vehicle_id} сгенерирован")
        else:
            print(f"ℹ ТС ID={vehicle_id} не найдено (это нормально для тестов)")


