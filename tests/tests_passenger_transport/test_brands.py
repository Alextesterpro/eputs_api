#!/usr/bin/env python3
"""
Тесты для Марок (Brands) в Пассажирском транспорте
"""

import pytest
import random


class TestBrands:
    """Тесты для марок"""
    
    def test_brands_list(self, passenger_transport_client):
        """Тест получения списка марок"""
        limit = 25
        result = passenger_transport_client.get_brands_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        brands = data.get("data", [])
        assert isinstance(brands, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(brands) <= limit, f"Количество элементов ({len(brands)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(brands) > 0:
            first_brand = brands[0]
            assert "id" in first_brand, "Отсутствует поле id"
            assert isinstance(first_brand["id"], int), "ID должен быть числом"
            
            if "name_ru" in first_brand:
                assert isinstance(first_brand["name_ru"], str), "Name_ru должен быть строкой"
            
            print(f"Пример марки: ID={first_brand['id']}, Name={first_brand.get('name_ru', 'N/A')}")
        
        print(f"Получено марок: {len(brands)}")


class TestBrandsCRUD:
    """CRUD тесты для марок"""
    
    def test_brand_workflow(self, passenger_transport_client):
        """Workflow: CREATE -> UPDATE -> DELETE марки"""
        
        # ===== Шаг 1: CREATE =====
        random_int = random.randint(1000, 9999)
        name_ru = f"Апи добавление {random_int}"
        name_en = f"Api {random_int}"
        slug = f"api-{random_int}"
        
        create_result = passenger_transport_client.create_brand(
            name_ru=name_ru,
            name_en=name_en,
            slug=slug,
            category_id=1
        )
        
        assert create_result.status_code == 200, "Шаг 1 (CREATE) failed"
        create_data = create_result.json()
        assert create_data.get("success") is True, "Шаг 1: нет success=true"
        
        brand_id = create_data["data"]["id"]
        print(f"✓ Шаг 1 (CREATE): марка ID={brand_id}, name_ru='{name_ru}'")
        
        # ===== Шаг 2: UPDATE =====
        updated_name_ru = f"Апи редактирование {random_int}"
        updated_name_en = f"Pai {random_int}"
        updated_slug = f"pai-{random_int}"
        
        update_result = passenger_transport_client.update_brand(
            brand_id=brand_id,
            name_ru=updated_name_ru,
            name_en=updated_name_en,
            slug=updated_slug,
            category_id=1
        )
        
        assert update_result.status_code == 200, "Шаг 2 (UPDATE) failed"
        update_data = update_result.json()
        assert update_data.get("success") is True, "Шаг 2: нет success=true"
        
        # Проверка что данные изменились
        if "data" in update_data and "name_ru" in update_data["data"]:
            assert update_data["data"]["name_ru"] == updated_name_ru, "Name_ru не обновился"
        
        print(f"✓ Шаг 2 (UPDATE): марка ID={brand_id} обновлена, new_name='{updated_name_ru}'")
        
        # ===== Шаг 3: DELETE =====
        delete_result = passenger_transport_client.delete_brand(brand_id)
        
        assert delete_result.status_code == 200, "Шаг 3 (DELETE) failed"
        delete_data = delete_result.json()
        assert delete_data.get("success") is True, "Шаг 3: нет success=true"
        
        print(f"✓ Шаг 3 (DELETE): марка ID={brand_id} удалена")
        print(f"\n✓ Workflow завершен успешно: CREATE -> UPDATE -> DELETE")


