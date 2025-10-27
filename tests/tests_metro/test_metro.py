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
        result = metro_client.get_vestibules_on_page(page=1, limit=500)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Нет поля data в ответе"
        print(f"Vestibules on page: найдено {len(data.get('data', []))} вестибюлей")
    
    def test_vestibule_traffic_thresholds_list(self, metro_client):
        """Тест получения списка порогов пассажиропотока"""
        result = metro_client.get_vestibule_traffic_thresholds_list()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Vestibule traffic thresholds list работает")
    
    def test_vestibule_traffic_report(self, metro_client):
        """Тест получения отчета о пассажирах"""
        today = datetime.now()
        start_date = today.strftime("%Y-%m-%dT00:00:00+03:00")
        end_date = today.strftime("%Y-%m-%dT23:59:59+03:00")
        
        result = metro_client.get_vestibule_traffic_report(start_date, end_date)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Vestibule traffic report работает")
    
    def test_generate_passenger_report(self, metro_client):
        """Тест формирования отчета о пассажирах"""
        today = datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        
        result = metro_client.generate_passenger_report(
            start_date=date_str,
            end_date=date_str,
            formats=["HTML", "CSV", "XLSX"]
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Generate passenger report работает")


class TestMetroUpdate:
    """Тесты для обновления данных Метрополитен"""
    
    def test_update_vestibule_traffic_thresholds(self, metro_client):
        """Тест обновления порогов пассажиропотока"""
        # Сначала получаем список существующих порогов
        get_result = metro_client.get_vestibule_traffic_thresholds_list()
        assert get_result.status_code == 200, f"Не удалось получить список порогов: {get_result.status_code}"
        
        get_data = get_result.json()
        assert get_data.get("success") is True, "Не удалось получить список порогов"
        
        thresholds = get_data.get("data", [])
        if len(thresholds) == 0:
            pytest.skip("Нет порогов для обновления")
        
        # Берем первые 4 порога и обновляем их count
        import random
        updated_thresholds = []
        for threshold in thresholds[:4]:
            threshold_copy = threshold.copy()
            threshold_copy["count"] = random.randint(50, 150)
            updated_thresholds.append(threshold_copy)
        
        # Обновляем
        result = metro_client.update_vestibule_traffic_thresholds(updated_thresholds)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Обновление не прошло"
        print(f"Обновлено {len(updated_thresholds)} порогов пассажиропотока")


class TestMetroWorkflow:
    """Workflow тесты для Метрополитен"""
    
    def test_vestibules_workflow(self, metro_client):
        """Полный цикл работы с вестибюлями"""
        # 1. Получить список вестибюлей
        vestibules_result = metro_client.get_vestibules_on_page(page=1, limit=10)
        assert vestibules_result.status_code == 200
        vestibules_data = vestibules_result.json()
        assert vestibules_data.get("success") is True
        assert len(vestibules_data.get("data", [])) > 0, "Нет вестибюлей в системе"
        
        # 2. Получить пороги
        thresholds_result = metro_client.get_vestibule_traffic_thresholds_list()
        assert thresholds_result.status_code == 200
        thresholds_data = thresholds_result.json()
        assert thresholds_data.get("success") is True
        
        # 3. Получить отчет по пассажирам
        today = datetime.now()
        start_date = today.strftime("%Y-%m-%dT00:00:00+03:00")
        end_date = today.strftime("%Y-%m-%dT23:59:59+03:00")
        
        traffic_result = metro_client.get_vestibule_traffic_report(start_date, end_date)
        assert traffic_result.status_code == 200
        traffic_data = traffic_result.json()
        assert traffic_data.get("success") is True
        
        print("Workflow для вестибюлей метрополитена прошел успешно")

