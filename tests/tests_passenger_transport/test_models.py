#!/usr/bin/env python3
"""
Тесты для Моделей (Models) в Пассажирском транспорте
"""

import pytest
import random


class TestModels:
    """Тесты для моделей"""
    
    def test_models_list(self, passenger_transport_client):
        """Тест получения списка моделей"""
        limit = 25
        result = passenger_transport_client.get_models_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        models = data.get("data", [])
        assert isinstance(models, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(models) <= limit, f"Количество элементов ({len(models)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(models) > 0:
            first_model = models[0]
            assert "id" in first_model, "Отсутствует поле id"
            assert isinstance(first_model["id"], int), "ID должен быть числом"
            
            if "name_ru" in first_model:
                assert isinstance(first_model["name_ru"], str), "Name_ru должен быть строкой"
            
            print(f"Пример модели: ID={first_model['id']}, Name={first_model.get('name_ru', 'N/A')}")
        
        print(f"Получено моделей: {len(models)}")


class TestModelsCRUD:
    """CRUD тесты для моделей"""
    
    def test_model_workflow(self, passenger_transport_client):
        """Workflow: CREATE -> UPDATE -> DELETE модели"""
        
        # ===== Шаг 1: CREATE =====
        random_int = random.randint(1000, 9999)
        name_ru = f"Апи добавление {random_int}"
        name_en = f"Api {random_int}"
        slug = f"api-model-{random_int}"
        
        create_result = passenger_transport_client.create_model(
            brand_id=2,  # Используем существующую марку
            name_ru=name_ru,
            name_en=name_en,
            slug=slug
        )
        
        assert create_result.status_code == 200, "Шаг 1 (CREATE) failed"
        create_data = create_result.json()
        assert create_data.get("success") is True, "Шаг 1: нет success=true"
        
        model_id = create_data["data"]["id"]
        print(f"✓ Шаг 1 (CREATE): модель ID={model_id}, name_ru='{name_ru}'")
        
        # ===== Шаг 2: UPDATE =====
        updated_name_ru = f"Апи редактирование {random_int}"
        updated_name_en = f"Pai {random_int}"
        updated_slug = f"pai-model-{random_int}"
        
        update_result = passenger_transport_client.update_model(
            model_id=model_id,
            brand_id=2,
            name_ru=updated_name_ru,
            name_en=updated_name_en,
            slug=updated_slug
        )
        
        assert update_result.status_code == 200, "Шаг 2 (UPDATE) failed"
        update_data = update_result.json()
        assert update_data.get("success") is True, "Шаг 2: нет success=true"
        
        # Проверка что данные изменились
        if "data" in update_data and "name_ru" in update_data["data"]:
            assert update_data["data"]["name_ru"] == updated_name_ru, "Name_ru не обновился"
        
        print(f"✓ Шаг 2 (UPDATE): модель ID={model_id} обновлена, new_name='{updated_name_ru}'")
        
        # ===== Шаг 3: DELETE =====
        delete_result = passenger_transport_client.delete_model(model_id)
        
        assert delete_result.status_code == 200, "Шаг 3 (DELETE) failed"
        delete_data = delete_result.json()
        assert delete_data.get("success") is True, "Шаг 3: нет success=true"
        
        print(f"✓ Шаг 3 (DELETE): модель ID={model_id} удалена")
        print(f"\n✓ Workflow завершен успешно: CREATE -> UPDATE -> DELETE")


