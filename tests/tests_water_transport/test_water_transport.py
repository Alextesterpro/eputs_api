"""
Тесты для API Водного транспорта
"""
import pytest
import random


class TestWaterTransportVehicles:
    """Тесты для работы с транспортными средствами водного транспорта"""

    def test_vehicle_list(self, water_transport_client):
        """Тест получения списка транспортных средств"""
        response = water_transport_client.vehicle_list(page=1, limit=25)
        
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data.get("success") is True, "Нет success=true"
        print(f"Получено транспортных средств: {len(data.get('data', {}).get('items', []))}")

    def test_vehicle_list_pagination(self, water_transport_client):
        """Тест пагинации списка транспортных средств"""
        # Первая страница
        response_page1 = water_transport_client.vehicle_list(page=1, limit=10)
        assert response_page1.status_code == 200
        data_page1 = response_page1.json()
        assert data_page1.get("success") is True
        
        # Вторая страница
        response_page2 = water_transport_client.vehicle_list(page=2, limit=10)
        assert response_page2.status_code == 200
        data_page2 = response_page2.json()
        assert data_page2.get("success") is True
        
        print(f"Страница 1: {len(data_page1.get('data', {}).get('items', []))} элементов")
        print(f"Страница 2: {len(data_page2.get('data', {}).get('items', []))} элементов")

    def test_vehicle_create_update_delete(self, water_transport_client):
        """Тест полного цикла CRUD для транспортного средства"""
        # Генерация случайных данных
        random_int = random.randint(1000, 9999)
        mmsi = str(random.randint(100000000, 999999999))  # 9 цифр
        imo = str(random.randint(1000000, 9999999))  # 7 цифр
        
        # Создание
        response_create = water_transport_client.vehicle_create(
            name=f"Апи добавление {random_int}",
            short_name="Test Ship",
            mmsi=mmsi,
            imo=imo,
            vehicle_type="5"
        )
        
        assert response_create.status_code == 200, f"Create failed: {response_create.status_code}"
        create_data = response_create.json()
        assert create_data.get("success") is True, "Нет success=true при создании"
        
        vehicle_id = create_data.get("data", {}).get("id")
        assert vehicle_id is not None, "ID не вернулся после создания"
        print(f"Создано транспортное средство с ID: {vehicle_id}")
        
        # Обновление
        random_int_update = random.randint(1000, 9999)
        mmsi_update = str(random.randint(100000000, 999999999))
        imo_update = str(random.randint(1000000, 9999999))
        
        response_update = water_transport_client.vehicle_update(
            vehicle_id=vehicle_id,
            name=f"Апи редактирование {random_int_update}",
            short_name="Updated Ship",
            mmsi=mmsi_update,
            imo=imo_update,
            vehicle_type="5"
        )
        
        assert response_update.status_code == 200, f"Update failed: {response_update.status_code}"
        update_data = response_update.json()
        assert update_data.get("success") is True, "Нет success=true при обновлении"
        print(f"Обновлено транспортное средство ID: {vehicle_id}")
        
        # Удаление
        response_delete = water_transport_client.vehicle_delete(vehicle_id)
        
        assert response_delete.status_code == 200, f"Delete failed: {response_delete.status_code}"
        delete_data = response_delete.json()
        assert delete_data.get("success") is True, "Нет success=true при удалении"
        print(f"Удалено транспортное средство ID: {vehicle_id}")

    def test_vehicle_create_with_invalid_mmsi(self, water_transport_client):
        """Тест создания с некорректным MMSI (должен быть негативным)"""
        random_int = random.randint(1000, 9999)
        
        response = water_transport_client.vehicle_create(
            name=f"Invalid MMSI Test {random_int}",
            short_name="Test",
            mmsi="123",  # Некорректный MMSI (должен быть 9 цифр)
            imo=str(random.randint(1000000, 9999999)),
            vehicle_type="5"
        )
        
        # API может принять или отклонить - проверяем ответ
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        # Если создание прошло успешно, удаляем
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data", {}).get("id"):
                vehicle_id = data["data"]["id"]
                water_transport_client.vehicle_delete(vehicle_id)
                print(f"Очищено: удалено транспортное средство ID {vehicle_id}")

    def test_vehicle_create_with_invalid_imo(self, water_transport_client):
        """Тест создания с некорректным IMO (должен быть негативным)"""
        random_int = random.randint(1000, 9999)
        
        response = water_transport_client.vehicle_create(
            name=f"Invalid IMO Test {random_int}",
            short_name="Test",
            mmsi=str(random.randint(100000000, 999999999)),
            imo="123",  # Некорректный IMO (должен быть 7 цифр)
            vehicle_type="5"
        )
        
        # API может принять или отклонить - проверяем ответ
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        # Если создание прошло успешно, удаляем
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data", {}).get("id"):
                vehicle_id = data["data"]["id"]
                water_transport_client.vehicle_delete(vehicle_id)
                print(f"Очищено: удалено транспортное средство ID {vehicle_id}")

    def test_vehicle_delete_nonexistent(self, water_transport_client):
        """Тест удаления несуществующего транспортного средства"""
        nonexistent_id = 999999999
        
        response = water_transport_client.vehicle_delete(nonexistent_id)
        
        # Ожидаем ошибку или success=false
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        
        # Обычно API возвращает 404 или 200 с success=false
        if response.status_code == 200:
            data = response.json()
            # Либо success=false, либо сообщение об ошибке
            assert data.get("success") is False or "error" in data or "message" in data

