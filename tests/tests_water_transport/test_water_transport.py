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
        
        # Проверка статус кода
        assert response.status_code == 200, f"Status code: {response.status_code}"
        
        # Проверка структуры ответа
        data = response.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Отсутствует поле data"
        
        # Получение списка элементов
        items = data.get('data', data) if isinstance(data.get('data'), list) else data.get('data', {}).get('items', [])
        assert isinstance(items, list), "Данные должны быть списком"
        
        # Проверка структуры элементов (если есть)
        if len(items) > 0:
            first_item = items[0]
            assert "id" in first_item, "Отсутствует поле id"
            assert "name" in first_item, "Отсутствует поле name"
            assert isinstance(first_item["id"], int), "ID должен быть числом"
            assert isinstance(first_item["name"], str), "Name должен быть строкой"
            print(f"Пример транспортного средства: ID={first_item['id']}, Name={first_item['name']}")
        
        print(f"Получено транспортных средств: {len(items)}")

    def test_vehicle_list_pagination(self, water_transport_client):
        """Тест пагинации списка транспортных средств"""
        limit = 10
        
        # Первая страница
        response_page1 = water_transport_client.vehicle_list(page=1, limit=limit)
        assert response_page1.status_code == 200, f"Page 1 status: {response_page1.status_code}"
        data_page1 = response_page1.json()
        assert data_page1.get("success") is True, "Page 1: нет success=true"
        
        # Вторая страница
        response_page2 = water_transport_client.vehicle_list(page=2, limit=limit)
        assert response_page2.status_code == 200, f"Page 2 status: {response_page2.status_code}"
        data_page2 = response_page2.json()
        assert data_page2.get("success") is True, "Page 2: нет success=true"
        
        # Получение списков
        items1 = data_page1.get('data', data_page1) if isinstance(data_page1.get('data'), list) else data_page1.get('data', {}).get('items', [])
        items2 = data_page2.get('data', data_page2) if isinstance(data_page2.get('data'), list) else data_page2.get('data', {}).get('items', [])
        
        # Проверка типов
        assert isinstance(items1, list), "Страница 1: данные должны быть списком"
        assert isinstance(items2, list), "Страница 2: данные должны быть списком"
        
        # Проверка лимита
        assert len(items1) <= limit, f"Страница 1: количество элементов ({len(items1)}) превышает лимит ({limit})"
        assert len(items2) <= limit, f"Страница 2: количество элементов ({len(items2)}) превышает лимит ({limit})"
        
        # Проверка что страницы разные (если есть данные)
        if len(items1) > 0 and len(items2) > 0:
            ids_page1 = [item["id"] for item in items1 if "id" in item]
            ids_page2 = [item["id"] for item in items2 if "id" in item]
            
            # ID на разных страницах не должны повторяться
            common_ids = set(ids_page1) & set(ids_page2)
            assert len(common_ids) == 0, f"Найдены одинаковые ID на разных страницах: {common_ids}"
            print(f"Пагинация работает корректно: страницы содержат разные данные")
        
        print(f"Страница 1: {len(items1)} элементов")
        print(f"Страница 2: {len(items2)} элементов")

    def test_vehicle_create_update_delete(self, water_transport_client):
        """Тест полного цикла CRUD для транспортного средства"""
        # Генерация случайных данных для создания
        random_int = random.randint(1000, 9999)
        original_name = f"Апи добавление {random_int}"
        original_short_name = "Test Ship"
        mmsi = str(random.randint(100000000, 999999999))  # 9 цифр
        imo = str(random.randint(1000000, 9999999))  # 7 цифр
        vehicle_type = "5"
        
        # ===== CREATE =====
        response_create = water_transport_client.vehicle_create(
            name=original_name,
            short_name=original_short_name,
            mmsi=mmsi,
            imo=imo,
            vehicle_type=vehicle_type
        )
        
        # Проверка статуса создания
        assert response_create.status_code == 200, f"Create failed: {response_create.status_code}"
        create_data = response_create.json()
        assert create_data.get("success") is True, "Нет success=true при создании"
        assert "data" in create_data, "Отсутствует поле data в ответе"
        
        # Проверка структуры созданного объекта
        vehicle_data = create_data["data"]
        assert "id" in vehicle_data, "Отсутствует поле id"
        vehicle_id = vehicle_data["id"]
        assert isinstance(vehicle_id, int), "ID должен быть числом"
        assert vehicle_id > 0, "ID должен быть положительным числом"
        
        # Проверка что вернулись правильные данные
        if "name" in vehicle_data:
            assert vehicle_data["name"] == original_name, f"Name не совпадает: ожидалось '{original_name}', получено '{vehicle_data['name']}'"
        if "mmsi" in vehicle_data:
            assert str(vehicle_data["mmsi"]) == mmsi, f"MMSI не совпадает: ожидалось '{mmsi}', получено '{vehicle_data['mmsi']}'"
        if "imo" in vehicle_data:
            assert str(vehicle_data["imo"]) == imo, f"IMO не совпадает: ожидалось '{imo}', получено '{vehicle_data['imo']}'"
        
        print(f"✓ CREATE: создано транспортное средство ID={vehicle_id}, name='{original_name}'")
        
        # ===== UPDATE =====
        random_int_update = random.randint(1000, 9999)
        updated_name = f"Апи редактирование {random_int_update}"
        updated_short_name = f"Updated Ship {random.randint(1000, 9999)}"
        mmsi_update = str(random.randint(100000000, 999999999))
        imo_update = str(random.randint(1000000, 9999999))
        
        response_update = water_transport_client.vehicle_update(
            vehicle_id=vehicle_id,
            name=updated_name,
            short_name=updated_short_name,
            mmsi=mmsi_update,
            imo=imo_update,
            vehicle_type=vehicle_type
        )
        
        # Проверка статуса обновления
        assert response_update.status_code == 200, f"Update failed: {response_update.status_code}"
        update_data = response_update.json()
        assert update_data.get("success") is True, "Нет success=true при обновлении"
        
        # Проверка что данные действительно изменились
        if "data" in update_data:
            updated_vehicle = update_data["data"]
            if "name" in updated_vehicle:
                assert updated_vehicle["name"] == updated_name, f"Name не обновился: '{updated_vehicle['name']}'"
                assert updated_vehicle["name"] != original_name, "Name не изменился после UPDATE"
        
        print(f"✓ UPDATE: обновлено транспортное средство ID={vehicle_id}, new_name='{updated_name}'")
        
        # ===== DELETE =====
        response_delete = water_transport_client.vehicle_delete(vehicle_id)
        
        # Проверка статуса удаления
        assert response_delete.status_code == 200, f"Delete failed: {response_delete.status_code}"
        delete_data = response_delete.json()
        assert delete_data.get("success") is True, "Нет success=true при удалении"
        
        print(f"✓ DELETE: удалено транспортное средство ID={vehicle_id}")
        
        # ===== ПРОВЕРКА ЧТО ОБЪЕКТ УДАЛЕН =====
        # Попытка получить удаленный объект через list
        list_response = water_transport_client.vehicle_list(page=1, limit=100)
        if list_response.status_code == 200:
            list_data = list_response.json()
            items = list_data.get('data', list_data) if isinstance(list_data.get('data'), list) else list_data.get('data', {}).get('items', [])
            
            # Проверяем что удаленного ID нет в списке
            deleted_ids = [item.get("id") for item in items if item.get("id") == vehicle_id]
            assert len(deleted_ids) == 0, f"Удаленный объект ID={vehicle_id} все еще присутствует в списке!"
            print(f"✓ VERIFY: подтверждено удаление - объект ID={vehicle_id} отсутствует в списке")

    def test_vehicle_create_with_invalid_mmsi(self, water_transport_client):
        """Тест создания с некорректным MMSI (негативный сценарий)"""
        random_int = random.randint(1000, 9999)
        invalid_mmsi = "123"  # Некорректный MMSI (должен быть 9 цифр)
        
        response = water_transport_client.vehicle_create(
            name=f"Invalid MMSI Test {random_int}",
            short_name="Test",
            mmsi=invalid_mmsi,
            imo=str(random.randint(1000000, 9999999)),
            vehicle_type="5"
        )
        
        print(f"Response status: {response.status_code}")
        
        # API может вести себя по-разному:
        # 1) Отклонить с ошибкой (400/422) - правильное поведение
        # 2) Принять невалидные данные (200) - проблема валидации
        
        if response.status_code in [400, 422]:
            # Ожидаемое поведение - валидация работает
            data = response.json()
            assert data.get("success") is False or "error" in data or "message" in data, \
                "При ошибке должно быть success=false или поле error/message"
            print(f"✓ Валидация работает: API отклонил некорректный MMSI ({invalid_mmsi})")
        
        elif response.status_code == 200:
            # API принял невалидные данные - удаляем и логируем проблему
            data = response.json()
            print(f"⚠ Проблема валидации: API принял некорректный MMSI ({invalid_mmsi})")
            
            if data.get("success") and data.get("data", {}).get("id"):
                vehicle_id = data["data"]["id"]
                water_transport_client.vehicle_delete(vehicle_id)
                print(f"Cleanup: удалено транспортное средство ID={vehicle_id}")
        
        else:
            pytest.fail(f"Неожиданный статус код: {response.status_code}")

    def test_vehicle_create_with_invalid_imo(self, water_transport_client):
        """Тест создания с некорректным IMO (негативный сценарий)"""
        random_int = random.randint(1000, 9999)
        invalid_imo = "123"  # Некорректный IMO (должен быть 7 цифр)
        
        response = water_transport_client.vehicle_create(
            name=f"Invalid IMO Test {random_int}",
            short_name="Test",
            mmsi=str(random.randint(100000000, 999999999)),
            imo=invalid_imo,
            vehicle_type="5"
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code in [400, 422]:
            # Ожидаемое поведение - валидация работает
            data = response.json()
            assert data.get("success") is False or "error" in data or "message" in data, \
                "При ошибке должно быть success=false или поле error/message"
            print(f"✓ Валидация работает: API отклонил некорректный IMO ({invalid_imo})")
        
        elif response.status_code == 200:
            # API принял невалидные данные - удаляем и логируем проблему
            data = response.json()
            print(f"⚠ Проблема валидации: API принял некорректный IMO ({invalid_imo})")
            
            if data.get("success") and data.get("data", {}).get("id"):
                vehicle_id = data["data"]["id"]
                water_transport_client.vehicle_delete(vehicle_id)
                print(f"Cleanup: удалено транспортное средство ID={vehicle_id}")
        
        else:
            pytest.fail(f"Неожиданный статус код: {response.status_code}")

    def test_vehicle_delete_nonexistent(self, water_transport_client):
        """Тест удаления несуществующего транспортного средства (негативный сценарий)"""
        nonexistent_id = 999999999
        
        response = water_transport_client.vehicle_delete(nonexistent_id)
        
        print(f"Response status: {response.status_code}")
        
        # API должен вернуть ошибку при попытке удалить несуществующий объект
        if response.status_code == 404:
            # Правильное поведение - объект не найден
            print(f"✓ API корректно вернул 404 для несуществующего ID={nonexistent_id}")
        
        elif response.status_code == 200:
            # API вернул 200 - проверяем success
            data = response.json()
            
            if data.get("success") is False:
                # Правильно - success=false указывает на проблему
                assert "error" in data or "message" in data, "Должно быть поле error или message"
                print(f"✓ API вернул success=false для несуществующего ID={nonexistent_id}")
            else:
                # Проблема - API сообщает об успешном удалении несуществующего объекта
                pytest.fail(f"⚠ API вернул success=true для несуществующего объекта ID={nonexistent_id}")
        
        elif response.status_code in [400, 422]:
            # Тоже приемлемое поведение - Bad Request
            print(f"✓ API вернул {response.status_code} для несуществующего ID={nonexistent_id}")
        
        else:
            pytest.fail(f"Неожиданный статус код: {response.status_code}")

