"""
Negative test scenarios for Incidents API.
Tests invalid data, unauthorized access, and error conditions.
"""

import pytest
from typing import Dict, Any

from tests_microservices.utils.incidents.incidents_api import IncidentsAPI
from tests_microservices.utils.incidents.incident_schemas import (
    IncidentAssertions,
    IncidentTestData
)


@pytest.mark.negative
class TestIncidentNegative:
    """Negative test scenarios for incidents API."""

    def test_create_incident_empty_name(self):
        """Test incident creation with empty name."""
        # Arrange
        invalid_data = {
            "name": "",  # Empty name should fail
            "description": "Valid description",
            "category_id": 1
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_missing_required_fields(self):
        """Test incident creation with missing required fields."""
        # Arrange - missing name
        invalid_data = {
            "description": "Valid description",
            "category_id": 1
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_invalid_category_id(self):
        """Test incident creation with invalid category ID."""
        # Arrange
        invalid_data = {
            "name": "Valid Name",
            "description": "Valid description",
            "category_id": "invalid_category"  # Wrong type
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_invalid_priority(self):
        """Test incident creation with invalid priority value."""
        # Arrange
        invalid_data = {
            "name": "Valid Name",
            "description": "Valid description",
            "category_id": 1,
            "priority": "invalid_priority"  # Invalid enum value
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_invalid_status(self):
        """Test incident creation with invalid status value."""
        # Arrange
        invalid_data = {
            "name": "Valid Name",
            "description": "Valid description",
            "category_id": 1,
            "status": "invalid_status"  # Invalid enum value
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_negative_category_id(self):
        """Test incident creation with negative category ID."""
        # Arrange
        invalid_data = {
            "name": "Valid Name",
            "description": "Valid description",
            "category_id": -1  # Negative ID should be invalid
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_very_long_name(self):
        """Test incident creation with extremely long name."""
        # Arrange
        very_long_name = "A" * 1000  # Very long name
        invalid_data = {
            "name": very_long_name,
            "description": "Valid description",
            "category_id": 1
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_create_incident_sql_injection_attempt(self):
        """Test incident creation with SQL injection attempt."""
        # Arrange
        malicious_data = {
            "name": "'; DROP TABLE incidents; --",
            "description": "Valid description",
            "category_id": 1
        }
        
        # Act
        response = IncidentsAPI.create_incident(malicious_data)
        
        # Assert
        # Should either reject the request or sanitize the input
        assert response.status_code in [400, 422, 201], f"Unexpected response: {response.status_code}: {response.text}"

    def test_create_incident_xss_attempt(self):
        """Test incident creation with XSS attempt."""
        # Arrange
        malicious_data = {
            "name": "<script>alert('xss')</script>",
            "description": "Valid description",
            "category_id": 1
        }
        
        # Act
        response = IncidentsAPI.create_incident(malicious_data)
        
        # Assert
        # Should either reject the request or sanitize the input
        assert response.status_code in [400, 422, 201], f"Unexpected response: {response.status_code}: {response.text}"

    def test_get_incident_invalid_id_format(self):
        """Test getting incident with invalid ID format."""
        # Arrange
        invalid_id = "not_a_number"
        
        # Act
        response = IncidentsAPI.get_incident(invalid_id)
        
        # Assert
        assert response.status_code in [400, 404], f"Expected 400/404, got {response.status_code}: {response.text}"

    def test_get_incident_negative_id(self):
        """Test getting incident with negative ID."""
        # Arrange
        negative_id = -1
        
        # Act
        response = IncidentsAPI.get_incident(negative_id)
        
        # Assert
        assert response.status_code in [400, 404], f"Expected 400/404, got {response.status_code}: {response.text}"

    def test_update_incident_invalid_id(self):
        """Test updating incident with invalid ID."""
        # Arrange
        invalid_id = "not_a_number"
        update_data = {"name": "Updated Name"}
        
        # Act
        response = IncidentsAPI.update_incident(invalid_id, update_data)
        
        # Assert
        assert response.status_code in [400, 404], f"Expected 400/404, got {response.status_code}: {response.text}"

    def test_update_incident_empty_payload(self):
        """Test updating incident with empty payload."""
        # Arrange
        incident_id = 1
        empty_payload = {}
        
        # Act
        response = IncidentsAPI.update_incident(incident_id, empty_payload)
        
        # Assert
        # Should either accept empty payload or reject it
        assert response.status_code in [200, 201, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_update_incident_invalid_field_types(self):
        """Test updating incident with invalid field types."""
        # Arrange
        incident_id = 1
        invalid_payload = {
            "name": 123,  # Should be string
            "category_id": "not_a_number",  # Should be number
            "priority": 456  # Should be string
        }
        
        # Act
        response = IncidentsAPI.update_incident(incident_id, invalid_payload)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_delete_incident_invalid_id(self):
        """Test deleting incident with invalid ID."""
        # Arrange
        invalid_id = "not_a_number"
        
        # Act
        response = IncidentsAPI.delete_incident(invalid_id)
        
        # Assert
        assert response.status_code in [400, 404], f"Expected 400/404, got {response.status_code}: {response.text}"

    def test_list_incidents_invalid_pagination(self):
        """Test listing incidents with invalid pagination parameters."""
        # Arrange
        invalid_payload = {
            "page": -1,  # Negative page
            "limit": 0,  # Zero limit
            "is_simple": "not_a_boolean"  # Wrong type
        }
        
        # Act
        response = IncidentsAPI.list_incidents(invalid_payload)
        
        # Assert
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_list_incidents_very_large_limit(self):
        """Test listing incidents with very large limit."""
        # Arrange
        large_payload = {
            "page": 1,
            "limit": 10000,  # Very large limit
            "is_simple": True
        }
        
        # Act
        response = IncidentsAPI.list_incidents(large_payload)
        
        # Assert
        # Should either handle gracefully or return error
        assert response.status_code in [200, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_search_incidents_invalid_filters(self):
        """Test searching incidents with invalid filter values."""
        # Arrange
        invalid_payload = {
            "page": "not_a_number",
            "limit": "not_a_number",
            "category_id": "not_a_number",
            "status": 123,  # Should be string
            "priority": 456  # Should be string
        }
        
        # Act
        response = IncidentsAPI.search_incidents(invalid_payload)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"

    def test_search_incidents_sql_injection_in_search_term(self):
        """Test searching with SQL injection in search term."""
        # Arrange
        malicious_payload = {
            "search": "'; DROP TABLE incidents; --",
            "page": 1,
            "limit": 10
        }
        
        # Act
        response = IncidentsAPI.search_incidents(malicious_payload)
        
        # Assert
        # Should either reject the request or sanitize the input
        assert response.status_code in [200, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_search_incidents_xss_in_search_term(self):
        """Test searching with XSS in search term."""
        # Arrange
        malicious_payload = {
            "search": "<script>alert('xss')</script>",
            "page": 1,
            "limit": 10
        }
        
        # Act
        response = IncidentsAPI.search_incidents(malicious_payload)
        
        # Assert
        # Should either reject the request or sanitize the input
        assert response.status_code in [200, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"


@pytest.mark.negative
class TestIncidentSecurity:
    """Security-focused negative tests."""

    def test_unauthorized_access_without_token(self):
        """Test API access without authentication token."""
        # This test would require modifying the auth headers
        # For now, we'll test with invalid token
        invalid_headers = {
            "Authorization": "Bearer invalid_token_12345",
            "Content-Type": "application/json",
            "project": "98_spb",
            "service": "eputs"
        }
        
        # Act
        response = IncidentsAPI.list_incidents({"page": 1, "limit": 1}, headers=invalid_headers)
        
        # Assert
        assert response.status_code == 401, f"Expected 401 for invalid token, got {response.status_code}: {response.text}"

    def test_unauthorized_access_without_project_header(self):
        """Test API access without required project header."""
        # Arrange
        headers_without_project = {
            "Authorization": "Bearer valid_token",
            "Content-Type": "application/json",
            "service": "eputs"
            # Missing "project" header
        }
        
        # Act
        response = IncidentsAPI.list_incidents({"page": 1, "limit": 1}, headers=headers_without_project)
        
        # Assert
        # Should either work (if project is optional) or return error
        assert response.status_code in [200, 400, 401], f"Unexpected response: {response.status_code}: {response.text}"

    def test_unauthorized_access_without_service_header(self):
        """Test API access without required service header."""
        # Arrange
        headers_without_service = {
            "Authorization": "Bearer valid_token",
            "Content-Type": "application/json",
            "project": "98_spb"
            # Missing "service" header
        }
        
        # Act
        response = IncidentsAPI.list_incidents({"page": 1, "limit": 1}, headers=headers_without_service)
        
        # Assert
        # Should either work (if service is optional) or return error
        assert response.status_code in [200, 400, 401], f"Unexpected response: {response.status_code}: {response.text}"

    def test_malformed_json_payload(self):
        """Test API with malformed JSON payload."""
        # This test would require sending raw malformed JSON
        # For now, we'll test with invalid data types that might cause JSON issues
        invalid_data = {
            "name": None,  # None value might cause JSON serialization issues
            "description": None,
            "category_id": None
        }
        
        # Act
        response = IncidentsAPI.create_incident(invalid_data)
        
        # Assert
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}: {response.text}"


@pytest.mark.negative
class TestIncidentBoundaryConditions:
    """Test boundary conditions and edge cases."""

    def test_create_incident_maximum_field_lengths(self):
        """Test incident creation with maximum field lengths."""
        # Arrange
        max_length_data = {
            "name": "A" * 255,  # Maximum reasonable name length
            "description": "B" * 1000,  # Maximum reasonable description length
            "category_id": 1
        }
        
        # Act
        response = IncidentsAPI.create_incident(max_length_data)
        
        # Assert
        # Should either accept or reject based on field length limits
        assert response.status_code in [200, 201, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_search_with_special_characters(self):
        """Test search with special characters."""
        # Arrange
        special_chars_payload = {
            "search": "!@#$%^&*()_+-=[]{}|;':\",./<>?",
            "page": 1,
            "limit": 10
        }
        
        # Act
        response = IncidentsAPI.search_incidents(special_chars_payload)
        
        # Assert
        # Should handle special characters gracefully
        assert response.status_code in [200, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_search_with_unicode_characters(self):
        """Test search with Unicode characters."""
        # Arrange
        unicode_payload = {
            "search": "тест инцидент 🚨",  # Cyrillic and emoji
            "page": 1,
            "limit": 10
        }
        
        # Act
        response = IncidentsAPI.search_incidents(unicode_payload)
        
        # Assert
        # Should handle Unicode characters gracefully
        assert response.status_code in [200, 400, 422], f"Unexpected response: {response.status_code}: {response.text}"

    def test_pagination_boundary_conditions(self):
        """Test pagination with boundary values."""
        # Test cases
        test_cases = [
            {"page": 0, "limit": 1},  # Zero page
            {"page": 1, "limit": 0},  # Zero limit
            {"page": 999999, "limit": 1},  # Very large page
            {"page": 1, "limit": 1},  # Minimum valid values
        ]
        
        for test_case in test_cases:
            # Act
            response = IncidentsAPI.list_incidents(test_case)
            
            # Assert
            # Should handle boundary conditions gracefully
            assert response.status_code in [200, 400, 422], f"Unexpected response for {test_case}: {response.status_code}: {response.text}"
