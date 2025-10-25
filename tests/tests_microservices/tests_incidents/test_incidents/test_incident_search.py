"""
Search and filtering tests for Incidents API.
Based on Postman collection with comprehensive search scenarios.
"""

import pytest
from typing import Dict, Any, List

from tests_microservices.utils.incidents.incidents_api import IncidentsAPI
from tests_microservices.utils.incidents.incident_schemas import (
    IncidentData,
    IncidentTestData,
    IncidentAssertions,
    IncidentListRequest,
    IncidentSearchRequest
)


@pytest.mark.basic
class TestIncidentSearch:
    """Search and filtering tests for incidents API."""

    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Setup test data for search tests."""
        self.test_incidents: List[int] = []
        yield
        # Cleanup: delete test incidents
        for incident_id in self.test_incidents:
            try:
                IncidentsAPI.delete_incident(incident_id)
            except Exception:
                pass  # Ignore cleanup errors

    def _create_test_incident(self, name: str, description: str, category_id: int = 1, 
                            priority: str = "medium", status: str = "open") -> int:
        """Helper to create test incident and return ID."""
        incident_data = IncidentData(
            name=name,
            description=description,
            category_id=category_id,
            priority=priority,
            status=status
        )
        
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        assert response.status_code in [200, 201], f"Failed to create test incident: {response.text}"
        
        created_incident = response.json()
        incident_id = created_incident["id"]
        self.test_incidents.append(incident_id)
        return incident_id

    def test_list_incidents_basic(self):
        """Test basic incident listing."""
        # Arrange
        list_request = IncidentTestData.create_list_request()
        
        # Act
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        # Assert
        list_data = IncidentAssertions.assert_incident_list(response)
        
        # Validate response structure
        assert "data" in list_data
        assert isinstance(list_data["data"], list)

    def test_list_incidents_pagination(self):
        """Test incident listing with pagination."""
        # Arrange
        list_request = IncidentListRequest(page=1, limit=5, is_simple=True)
        
        # Act
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        # Assert
        list_data = IncidentAssertions.assert_incident_list(response)
        
        # Validate pagination
        assert len(list_data["data"]) <= 5, "Should respect limit parameter"
        
        # Check pagination metadata if available
        if "total" in list_data:
            assert list_data["total"] >= 0, "Total count should be non-negative"
        if "page" in list_data:
            assert list_data["page"] == 1, "Page should match request"

    def test_list_incidents_by_category(self):
        """Test incident listing filtered by category."""
        # Arrange - create test incident with specific category
        test_category_id = 1
        self._create_test_incident("Category Test Incident", "Test for category filtering", test_category_id)
        
        list_request = IncidentListRequest(page=1, limit=10, is_simple=True, category_id=test_category_id)
        
        # Act
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        # Assert
        list_data = IncidentAssertions.assert_incident_list(response)
        
        # Validate all returned incidents have the correct category
        for incident in list_data["data"]:
            assert incident["category_id"] == test_category_id, f"Expected category {test_category_id}, got {incident['category_id']}"

    def test_list_incidents_by_status(self):
        """Test incident listing filtered by status."""
        # Arrange - create test incident with specific status
        test_status = "open"
        self._create_test_incident("Status Test Incident", "Test for status filtering", status=test_status)
        
        list_request = IncidentListRequest(page=1, limit=10, is_simple=True, status=test_status)
        
        # Act
        response = IncidentsAPI.list_incidents(list_request.to_dict())
        
        # Assert
        list_data = IncidentAssertions.assert_incident_list(response)
        
        # Validate all returned incidents have the correct status
        for incident in list_data["data"]:
            assert incident["status"] == test_status, f"Expected status {test_status}, got {incident['status']}"

    def test_search_incidents_by_text(self):
        """Test incident search by text query."""
        # Arrange - create test incident with searchable text
        search_term = "searchable_test_incident"
        self._create_test_incident(f"Test {search_term} Name", f"Description with {search_term}")
        
        search_request = IncidentSearchRequest(page=1, limit=10, search=search_term)
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        search_data = IncidentAssertions.assert_incident_search(response, search_term)
        
        # Validate search results contain the search term
        assert len(search_data["data"]) > 0, "Search should return results for existing term"

    def test_search_incidents_by_category(self):
        """Test incident search filtered by category."""
        # Arrange - create test incident with specific category
        test_category_id = 1
        self._create_test_incident("Category Search Test", "Test for category search", test_category_id)
        
        search_request = IncidentSearchRequest(page=1, limit=10, category_id=test_category_id)
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        search_data = IncidentAssertions.assert_incident_search(response)
        
        # Validate all returned incidents have the correct category
        for incident in search_data["data"]:
            assert incident["category_id"] == test_category_id, f"Expected category {test_category_id}, got {incident['category_id']}"

    def test_search_incidents_by_status(self):
        """Test incident search filtered by status."""
        # Arrange - create test incident with specific status
        test_status = "open"
        self._create_test_incident("Status Search Test", "Test for status search", status=test_status)
        
        search_request = IncidentSearchRequest(page=1, limit=10, status=test_status)
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        search_data = IncidentAssertions.assert_incident_search(response)
        
        # Validate all returned incidents have the correct status
        for incident in search_data["data"]:
            assert incident["status"] == test_status, f"Expected status {test_status}, got {incident['status']}"

    def test_search_incidents_by_priority(self):
        """Test incident search filtered by priority."""
        # Arrange - create test incident with specific priority
        test_priority = "high"
        self._create_test_incident("Priority Search Test", "Test for priority search", priority=test_priority)
        
        search_request = IncidentSearchRequest(page=1, limit=10, priority=test_priority)
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        search_data = IncidentAssertions.assert_incident_search(response)
        
        # Validate all returned incidents have the correct priority
        for incident in search_data["data"]:
            assert incident["priority"] == test_priority, f"Expected priority {test_priority}, got {incident['priority']}"

    def test_search_incidents_combined_filters(self):
        """Test incident search with multiple filters."""
        # Arrange - create test incident with specific attributes
        test_category_id = 1
        test_status = "open"
        test_priority = "medium"
        search_term = "combined_test"
        
        self._create_test_incident(
            f"Combined {search_term} Test",
            f"Description with {search_term}",
            category_id=test_category_id,
            priority=test_priority,
            status=test_status
        )
        
        search_request = IncidentSearchRequest(
            page=1,
            limit=10,
            search=search_term,
            category_id=test_category_id,
            status=test_status,
            priority=test_priority
        )
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        search_data = IncidentAssertions.assert_incident_search(response, search_term)
        
        # Validate all returned incidents match all filters
        for incident in search_data["data"]:
            assert incident["category_id"] == test_category_id, "Category filter not applied"
            assert incident["status"] == test_status, "Status filter not applied"
            assert incident["priority"] == test_priority, "Priority filter not applied"

    def test_search_incidents_empty_results(self):
        """Test search with filters that should return no results."""
        # Arrange - search for non-existent text
        search_request = IncidentSearchRequest(
            page=1,
            limit=10,
            search="non_existent_search_term_12345"
        )
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        search_data = response.json()
        assert "data" in search_data
        assert len(search_data["data"]) == 0, "Search should return empty results for non-existent term"

    def test_search_incidents_pagination(self):
        """Test search with pagination parameters."""
        # Arrange
        search_request = IncidentSearchRequest(page=2, limit=3)
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        search_data = response.json()
        assert "data" in search_data
        assert len(search_data["data"]) <= 3, "Should respect limit parameter"
        
        # Check pagination metadata if available
        if "page" in search_data:
            assert search_data["page"] == 2, "Page should match request"

    def test_list_vs_search_consistency(self):
        """Test that list and search endpoints return consistent data structure."""
        # Arrange
        list_request = IncidentListRequest(page=1, limit=5, is_simple=True)
        search_request = IncidentSearchRequest(page=1, limit=5)
        
        # Act
        list_response = IncidentsAPI.list_incidents(list_request.to_dict())
        search_response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        assert list_response.status_code == 200, "List endpoint should work"
        assert search_response.status_code == 200, "Search endpoint should work"
        
        list_data = list_response.json()
        search_data = search_response.json()
        
        # Both should have 'data' field
        assert "data" in list_data, "List response should have 'data' field"
        assert "data" in search_data, "Search response should have 'data' field"
        
        # Both should return lists
        assert isinstance(list_data["data"], list), "List response data should be a list"
        assert isinstance(search_data["data"], list), "Search response data should be a list"


@pytest.mark.regression
class TestIncidentSearchRegression:
    """Regression tests for search functionality."""

    def test_search_performance(self):
        """Test search performance with reasonable timeout."""
        import time
        
        # Arrange
        search_request = IncidentSearchRequest(page=1, limit=50)
        
        # Act
        start_time = time.time()
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200, f"Search failed: {response.text}"
        
        response_time = end_time - start_time
        assert response_time < 10.0, f"Search took too long: {response_time:.2f}s"
        
        print(f"Search completed in {response_time:.2f}s")

    def test_large_result_set_handling(self):
        """Test handling of large result sets."""
        # Arrange - request large number of results
        search_request = IncidentSearchRequest(page=1, limit=100)
        
        # Act
        response = IncidentsAPI.search_incidents(search_request.to_dict())
        
        # Assert
        assert response.status_code == 200, f"Large result set failed: {response.text}"
        
        search_data = response.json()
        assert "data" in search_data
        assert len(search_data["data"]) <= 100, "Should respect limit even for large requests"
