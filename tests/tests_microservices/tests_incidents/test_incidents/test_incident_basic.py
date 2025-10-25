"""
Базовые тесты для API инцидентов.
Обновлённые тесты с использованием новой архитектуры и POM.
"""

import json
import os
import pytest

from tests_microservices.utils.incidents.incidents_api import IncidentsAPI
from tests_microservices.utils.incidents.incident_schemas import (
    IncidentTestData,
    IncidentAssertions,
    IncidentListRequest,
    IncidentSearchRequest
)


@pytest.mark.basic

class TestIncidentsBasic:
    """Базовые smoke/basic тесты с улучшенной архитектурой."""

    def test_list_incidents_basic(self):
        """POST /incident/list — базовый тест получения списка"""
        list_request = IncidentListRequest(page=1, limit=10, is_simple=True)
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        assert response.status_code == 200, f"List request failed: {response.text}"
        data = response.json()
        assert "data" in data, "Response should contain 'data' field"
        assert isinstance(data["data"], list), "Data should be a list"

    def test_get_incident_by_id(self):
        """GET /incident/{id} — проверяем получение по ID"""
        incident_id = 2  # Предполагаем, что инцидент с ID 2 существует
        response = IncidentsAPI.get_incident(incident_id)
        
        # Допускаем как 200 (найден), так и 404 (не найден)
        assert response.status_code in (200, 404), f"Unexpected status: {response.status_code}"
        
        if response.status_code == 200:
            data = response.json()
            assert "id" in data, "Response should contain incident ID"
            assert data["id"] == incident_id, "Returned ID should match requested ID"

    def test_search_incidents_basic(self):
        """POST /incident/search — базовый тест поиска"""
        search_request = IncidentSearchRequest(page=1, limit=10, search="test")
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        assert response.status_code == 200, f"Search request failed: {response.text}"
        data = response.json()
        assert "data" in data, "Search response should contain 'data' field"
        assert isinstance(data["data"], list), "Search data should be a list"

    def test_list_incidents_pagination(self):
        """POST /incident/list — тест пагинации"""
        list_request = IncidentListRequest(page=1, limit=5, is_simple=True)
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        assert response.status_code == 200, f"Pagination test failed: {response.text}"
        data = response.json()
        assert "data" in data, "Response should contain 'data' field"
        
        items = data.get("data", [])
        assert len(items) <= 5, f"Should respect limit parameter, got {len(items)} items"

    def test_list_incidents_by_category(self):
        """POST /incident/list — фильтрация по категории"""
        list_request = IncidentListRequest(page=1, limit=10, is_simple=True, category_id=1)
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        assert response.status_code == 200, f"Category filter test failed: {response.text}"
        data = response.json()
        
        # Проверяем, что все возвращённые инциденты имеют правильную категорию
        for incident in data.get("data", []):
            assert incident.get("category_id") == 1, f"Expected category 1, got {incident.get('category_id')}"

    def test_search_incidents_by_text(self):
        """POST /incident/search — поиск по тексту"""
        search_request = IncidentSearchRequest(page=1, limit=10, search="incident")
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        assert response.status_code == 200, f"Text search failed: {response.text}"
        data = response.json()
        assert "data" in data, "Search response should contain 'data' field"

    def test_get_incident_invalid_id(self):
        """GET /incident/{id} — несуществующий ID"""
        response = IncidentsAPI.get_incident(99999999)
        assert response.status_code in (404, 400), f"Expected 404/400, got {response.status_code}"

    def test_search_incidents_empty_results(self):
        """POST /incident/search — поиск с пустыми результатами"""
        search_request = IncidentSearchRequest(
            page=1, 
            limit=10, 
            search="non_existent_search_term_12345"
        )
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        assert response.status_code == 200, f"Empty search failed: {response.text}"
        data = response.json()
        assert len(data.get("data", [])) == 0, "Search should return empty results for non-existent term"

    def test_api_connectivity(self):
        """Проверка базовой связности API"""
        list_request = IncidentListRequest(page=1, limit=1, is_simple=True)
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        # Не должно быть ошибок сервера или авторизации
        assert response.status_code not in (401, 500), f"API connectivity issue: {response.status_code}"
        assert response.status_code in (200, 404), f"Unexpected status: {response.status_code}"

    def test_authentication_working(self):
        """Проверка работы аутентификации"""
        # Пробуем создать инцидент (требует авторизации)
        incident_data = IncidentTestData.create_minimal_incident()
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        
        # Не должно быть 401 (неавторизован)
        assert response.status_code != 401, "Authentication failed - check token"
        
        # Если успешно создали, удаляем
        if response.status_code in (200, 201):
            created_incident = response.json()
            incident_id = created_incident.get("id")
            if incident_id:
                try:
                    IncidentsAPI.delete_incident(incident_id)
                except Exception:
                    pass  # Игнорируем ошибки очистки


@pytest.mark.smoke
class TestIncidentsSmoke:
    """Smoke тесты для критической функциональности."""

    def test_incident_api_health(self):
        """Проверка здоровья API инцидентов"""
        list_request = IncidentListRequest(page=1, limit=1, is_simple=True)
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        # API должен отвечать (200 или 404 - нормально)
        assert response.status_code in (200, 404), f"API health check failed: {response.status_code}"
        
        # Время ответа должно быть разумным
        assert response.elapsed.total_seconds() < 10.0, f"API response too slow: {response.elapsed.total_seconds()}s"

    def test_incident_endpoints_accessible(self):
        """Проверка доступности основных эндпоинтов"""
        endpoints_to_test = [
            ("list", lambda: IncidentsAPI.list_incidents({"page": 1, "limit": 1, "is_simple": True})),
            ("search", lambda: IncidentsAPI.search_incidents({"page": 1, "limit": 1, "search": "test"})),
            ("get", lambda: IncidentsAPI.get_incident(1))
        ]
        
        for endpoint_name, endpoint_func in endpoints_to_test:
            try:
                response = endpoint_func()
                assert response.status_code in (200, 404), f"{endpoint_name} endpoint failed: {response.status_code}"
            except Exception as e:
                pytest.fail(f"{endpoint_name} endpoint error: {e}")

    def test_incident_response_structure(self):
        """Проверка структуры ответов API"""
        list_request = IncidentListRequest(page=1, limit=1, is_simple=True)
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        if response.status_code == 200:
            data = response.json()
            assert "data" in data, "List response should have 'data' field"
            assert isinstance(data["data"], list), "Data should be a list"
            
            # Если есть данные, проверяем структуру первого элемента
            if data["data"]:
                incident = data["data"][0]
                required_fields = ["id", "name", "description", "category_id"]
                for field in required_fields:
                    assert field in incident, f"Incident should have '{field}' field"


