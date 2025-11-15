#!/usr/bin/env python3
"""
Тесты для раздела Метрополитен
"""

import pytest
from datetime import datetime, timedelta


class TestMetro:
    """Тесты для раздела Метрополитен"""
    
    def test_vestibules_on_page_list(self, metro_client):
        """Тест получения списка вестибюлей на странице"""
        limit = 500
        result = metro_client.get_vestibules_on_page(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        vestibules = data.get("data", [])
        assert isinstance(vestibules, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(vestibules) <= limit, f"Количество элементов ({len(vestibules)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(vestibules) > 0:
            first_vestibule = vestibules[0]
            assert "id" in first_vestibule or "name" in first_vestibule, "Отсутствуют ключевые поля"
            
            # Проверяем типы данных ключевых полей
            if "id" in first_vestibule:
                assert isinstance(first_vestibule["id"], int), "ID должен быть числом"
            if "name" in first_vestibule:
                assert isinstance(first_vestibule["name"], str), "Name должен быть строкой"
            
            print(f"Пример вестибюля: {first_vestibule.get('name', f'ID={first_vestibule.get('id')}')}")
        
        print(f"Получено вестибюлей: {len(vestibules)}")
    
    def test_vestibule_traffic_thresholds_list(self, metro_client):
        """Тест получения списка порогов пассажиропотока"""
        result = metro_client.get_vestibule_traffic_thresholds_list()
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка данных
        if "data" in data:
            thresholds = data.get("data", [])
            assert isinstance(thresholds, list), "Thresholds должны быть списком"
            
            # Проверка структуры элементов
            if len(thresholds) > 0:
                first_threshold = thresholds[0]
                
                # Проверяем ключевые поля
                if "count" in first_threshold:
                    assert isinstance(first_threshold["count"], (int, float)), "Count должен быть числом"
                    assert first_threshold["count"] >= 0, "Count должен быть неотрицательным"
                
                print(f"Пример порога: {first_threshold}")
            
            print(f" Получено порогов: {len(thresholds)}")
        else:
            print(" Список порогов: success=true")
    
    def test_vestibule_traffic_report(self, metro_client):
        """Тест получения отчета о пассажиропотоке"""
        today = datetime.now()
        start_date = today.strftime("%Y-%m-%dT00:00:00+03:00")
        end_date = today.strftime("%Y-%m-%dT23:59:59+03:00")
        
        # Запрос отчета
        result = metro_client.get_vestibule_traffic_report(start_date, end_date)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка данных отчета
        if "data" in data:
            report_data = data.get("data")
            assert report_data is not None, "Данные отчета не должны быть None"
            
            # Если это список, проверяем элементы
            if isinstance(report_data, list):
                if len(report_data) > 0:
                    first_item = report_data[0]
                    # Проверяем что есть какие-то данные о пассажирах
                    assert len(first_item) > 0, "Элементы отчета не должны быть пустыми"
                print(f" Отчет о пассажиропотоке: {len(report_data)} записей за {today.strftime('%Y-%m-%d')}")
            else:
                print(f" Отчет о пассажиропотоке: получены данные, тип={type(report_data).__name__}")
        else:
            print(" Отчет о пассажиропотоке: success=true")
    
    def test_generate_passenger_report(self, metro_client):
        """Тест генерации отчета о пассажирах в разных форматах"""
        today = datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        formats = ["HTML", "CSV", "XLSX"]
        
        # Генерация отчета
        result = metro_client.generate_passenger_report(
            start_date=date_str,
            end_date=date_str,
            formats=formats
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка что отчет был сгенерирован
        if "data" in data:
            report_info = data.get("data")
            
            # Проверяем что есть информация о сгенерированных файлах или ссылках
            if isinstance(report_info, dict):
                # Может быть поле с ссылками на файлы или статусом
                print(f" Отчет сгенерирован: {report_info}")
            elif isinstance(report_info, list):
                print(f" Отчет сгенерирован: {len(report_info)} файлов")
            else:
                print(f" Отчет сгенерирован: данные получены")
        else:
            print(f" Отчет сгенерирован для {date_str} в форматах: {', '.join(formats)}")


class TestMetroUpdate:
    """Тесты для обновления данных Метрополитен"""
    
    def test_update_vestibule_traffic_thresholds(self, metro_client):
        """Тест обновления порогов пассажиропотока"""
        import random
        
        # Получаем список существующих порогов
        get_result = metro_client.get_vestibule_traffic_thresholds_list()
        assert get_result.status_code == 200, f"Не удалось получить список: {get_result.status_code}"
        
        get_data = get_result.json()
        assert get_data.get("success") is True, "Не удалось получить список порогов"
        
        thresholds = get_data.get("data", [])
        if len(thresholds) == 0:
            pytest.skip("Нет порогов для обновления")
        
        # Берем первые 4 порога и обновляем их count
        original_counts = {}
        updated_thresholds = []
        
        for threshold in thresholds[:4]:
            threshold_copy = threshold.copy()
            original_count = threshold_copy.get("count", 0)
            new_count = random.randint(50, 150)
            
            # Сохраняем оригинальное значение для проверки
            if "id" in threshold_copy:
                original_counts[threshold_copy["id"]] = original_count
            
            threshold_copy["count"] = new_count
            updated_thresholds.append(threshold_copy)
        
        # Обновляем
        result = metro_client.update_vestibule_traffic_thresholds(updated_thresholds)
        
        # Проверка статуса
        assert result.status_code == 200, f"Update failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true при обновлении"
        
        print(f" UPDATE: обновлено {len(updated_thresholds)} порогов пассажиропотока")
        
        # Проверяем что значения действительно изменились (опционально)
        verify_result = metro_client.get_vestibule_traffic_thresholds_list()
        if verify_result.status_code == 200:
            verify_data = verify_result.json()
            if verify_data.get("success") and "data" in verify_data:
                updated_from_api = {t["id"]: t.get("count") for t in verify_data["data"] if "id" in t}
                
                changes_verified = 0
                for threshold in updated_thresholds:
                    if "id" in threshold:
                        threshold_id = threshold["id"]
                        expected_count = threshold["count"]
                        actual_count = updated_from_api.get(threshold_id)
                        
                        if actual_count == expected_count:
                            changes_verified += 1
                
                if changes_verified > 0:
                    print(f" VERIFY: подтверждено изменение {changes_verified} порогов")


class TestMetroWorkflow:
    """Workflow тесты для Метрополитен"""
    
    def test_vestibules_workflow(self, metro_client):
        """Полный workflow работы с вестибюлями метрополитена"""
        
        # ===== Шаг 1: Получить список вестибюлей =====
        vestibules_result = metro_client.get_vestibules_on_page(page=1, limit=10)
        assert vestibules_result.status_code == 200, f"Шаг 1 failed: {vestibules_result.status_code}"
        
        vestibules_data = vestibules_result.json()
        assert vestibules_data.get("success") is True, "Шаг 1: нет success=true"
        
        vestibules = vestibules_data.get("data", [])
        assert len(vestibules) > 0, "Нет вестибюлей в системе"
        
        print(f" Шаг 1: Получено {len(vestibules)} вестибюлей")
        
        # ===== Шаг 2: Получить пороги пассажиропотока =====
        thresholds_result = metro_client.get_vestibule_traffic_thresholds_list()
        assert thresholds_result.status_code == 200, f"Шаг 2 failed: {thresholds_result.status_code}"
        
        thresholds_data = thresholds_result.json()
        assert thresholds_data.get("success") is True, "Шаг 2: нет success=true"
        
        thresholds = thresholds_data.get("data", [])
        print(f" Шаг 2: Получено {len(thresholds)} порогов пассажиропотока")
        
        # ===== Шаг 3: Получить отчет по пассажирам =====
        today = datetime.now()
        start_date = today.strftime("%Y-%m-%dT00:00:00+03:00")
        end_date = today.strftime("%Y-%m-%dT23:59:59+03:00")
        
        traffic_result = metro_client.get_vestibule_traffic_report(start_date, end_date)
        assert traffic_result.status_code == 200, f"Шаг 3 failed: {traffic_result.status_code}"
        
        traffic_data = traffic_result.json()
        assert traffic_data.get("success") is True, "Шаг 3: нет success=true"
        
        print(f" Шаг 3: Получен отчет за {today.strftime('%Y-%m-%d')}")
        
        # ===== Итоговая проверка workflow =====
        print(f"\n Workflow завершен успешно: {len(vestibules)} вестибюлей, {len(thresholds)} порогов, отчет получен")

