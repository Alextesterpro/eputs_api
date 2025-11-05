#!/usr/bin/env python3
"""
Тесты для Jobs (Задачи)
"""

import pytest


class TestJobs:
    """Тесты для задач"""
    
    def test_jobs_list(self, data_bus_client):
        """Тест получения списка задач"""
        response = data_bus_client.job_list()
        
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Отсутствует поле data"
        
        # Проверяем структуру данных если они есть
        if isinstance(data["data"], list) and len(data["data"]) > 0:
            job = data["data"][0]
            assert "id" in job, "Отсутствует поле id в задаче"
            assert isinstance(job["id"], int), "ID задачи должен быть числом"

