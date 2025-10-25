"""
Pytest fixtures for incident API tests.
Provides test data setup, cleanup, and common utilities.
"""

import pytest
import os
from typing import List, Dict, Any, Generator
from datetime import datetime

from tests_microservices.utils.incidents.incidents_api import IncidentsAPI
from tests_microservices.utils.incidents.incident_schemas import (
    IncidentData,
    IncidentTestData,
    IncidentListRequest,
    IncidentSearchRequest
)


@pytest.fixture(scope="session")
def api_base_url():
    """Get API base URL from configuration."""
    from config.auth import AuthConfig
    return AuthConfig.API_BASE_URL


@pytest.fixture(scope="session")
def auth_headers():
    """Get authentication headers."""
    from config.auth import auth_manager
    return auth_manager.get_headers()


@pytest.fixture
def incident_cleanup():
    """Fixture to track and cleanup created incidents."""
    created_incidents: List[int] = []
    
    def add_incident(incident_id: int):
        """Add incident ID to cleanup list."""
        created_incidents.append(incident_id)
    
    def cleanup_all():
        """Cleanup all tracked incidents."""
        for incident_id in created_incidents:
            try:
                IncidentsAPI.delete_incident(incident_id)
            except Exception:
                pass  # Ignore cleanup errors
        created_incidents.clear()
    
    yield add_incident
    
    # Cleanup after test
    cleanup_all()


@pytest.fixture
def test_incident_data():
    """Fixture providing test incident data."""
    return {
        "valid": IncidentTestData.create_valid_incident(),
        "minimal": IncidentTestData.create_minimal_incident(),
        "full": IncidentTestData.create_incident_with_all_fields(),
        "invalid": IncidentTestData.create_invalid_incident()
    }


@pytest.fixture
def test_search_data():
    """Fixture providing test search data."""
    return {
        "basic_search": IncidentSearchRequest(page=1, limit=10, search="test"),
        "category_search": IncidentSearchRequest(page=1, limit=10, category_id=1),
        "status_search": IncidentSearchRequest(page=1, limit=10, status="open"),
        "complex_search": IncidentSearchRequest(
            page=1, limit=10, search="test", category_id=1, status="open", priority="high"
        )
    }


@pytest.fixture
def test_list_data():
    """Fixture providing test list data."""
    return {
        "basic_list": IncidentListRequest(page=1, limit=10, is_simple=True),
        "pagination": IncidentListRequest(page=1, limit=5, is_simple=True),
        "category_filter": IncidentListRequest(page=1, limit=10, is_simple=True, category_id=1),
        "status_filter": IncidentListRequest(page=1, limit=10, is_simple=True, status="open")
    }


@pytest.fixture
def sample_incident(incident_cleanup):
    """Fixture that creates a sample incident for testing."""
    incident_data = IncidentTestData.create_valid_incident()
    response = IncidentsAPI.create_incident(incident_data.to_dict())
    
    if response.status_code in [200, 201]:
        created_incident = response.json()
        incident_id = created_incident["id"]
        incident_cleanup(incident_id)
        
        yield {
            "id": incident_id,
            "data": created_incident,
            "original_data": incident_data
        }
    else:
        pytest.skip(f"Failed to create sample incident: {response.status_code} - {response.text}")


@pytest.fixture
def multiple_incidents(incident_cleanup):
    """Fixture that creates multiple sample incidents for testing."""
    incidents = []
    
    # Create 3 test incidents
    for i in range(3):
        incident_data = IncidentData(
            name=f"Test Incident {i+1}",
            description=f"Test description {i+1}",
            category_id=1,
            priority=["low", "medium", "high"][i],
            status=["open", "in_progress", "closed"][i]
        )
        
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        
        if response.status_code in [200, 201]:
            created_incident = response.json()
            incident_id = created_incident["id"]
            incident_cleanup(incident_id)
            incidents.append({
                "id": incident_id,
                "data": created_incident,
                "original_data": incident_data
            })
    
    if not incidents:
        pytest.skip("Failed to create any test incidents")
    
    yield incidents


@pytest.fixture
def incident_categories():
    """Fixture providing available incident categories."""
    # This would typically be fetched from the API
    # For now, return mock data
    return [
        {"id": 1, "name": "Security", "description": "Security-related incidents"},
        {"id": 2, "name": "Technical", "description": "Technical issues"},
        {"id": 3, "name": "Operational", "description": "Operational incidents"}
    ]


@pytest.fixture
def incident_priorities():
    """Fixture providing available incident priorities."""
    return ["low", "medium", "high", "critical"]


@pytest.fixture
def incident_statuses():
    """Fixture providing available incident statuses."""
    return ["open", "in_progress", "resolved", "closed", "cancelled"]


@pytest.fixture
def performance_thresholds():
    """Fixture providing performance thresholds for tests."""
    return {
        "max_response_time": 5.0,  # seconds
        "max_list_response_time": 3.0,
        "max_search_response_time": 5.0,
        "max_create_response_time": 10.0,
        "max_update_response_time": 8.0,
        "max_delete_response_time": 5.0,
        "min_success_rate": 0.95,  # 95%
        "max_concurrent_requests": 10
    }


@pytest.fixture
def test_environment():
    """Fixture providing test environment information."""
    return {
        "api_url": os.getenv("API_BASE_URL", "http://91.227.17.139/services/react/api"),
        "project": os.getenv("PROJECT", "98_spb"),
        "service": os.getenv("SERVICE", "eputs"),
        "has_token": bool(os.getenv("EPUTS_TOKEN")),
        "test_mode": os.getenv("TEST_MODE", "development")
    }


@pytest.fixture(scope="session")
def api_health_check():
    """Fixture to check API health before running tests."""
    try:
        # Try a simple list request to check API health
        response = IncidentsAPI.list_incidents({"page": 1, "limit": 1, "is_simple": True})
        
        if response.status_code in [200, 404]:
            return True
        else:
            pytest.skip(f"API health check failed: {response.status_code} - {response.text}")
    except Exception as e:
        pytest.skip(f"API health check failed: {e}")


@pytest.fixture
def incident_validation_rules():
    """Fixture providing validation rules for incident data."""
    return {
        "name": {
            "required": True,
            "min_length": 1,
            "max_length": 255,
            "type": str
        },
        "description": {
            "required": True,
            "min_length": 1,
            "max_length": 1000,
            "type": str
        },
        "category_id": {
            "required": True,
            "type": int,
            "min_value": 1
        },
        "priority": {
            "required": False,
            "type": str,
            "allowed_values": ["low", "medium", "high", "critical"]
        },
        "status": {
            "required": False,
            "type": str,
            "allowed_values": ["open", "in_progress", "resolved", "closed", "cancelled"]
        }
    }


@pytest.fixture
def test_data_generator():
    """Fixture providing test data generation utilities."""
    
    class TestDataGenerator:
        @staticmethod
        def generate_incident_name(prefix: str = "Test", suffix: str = "") -> str:
            """Generate unique incident name."""
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            return f"{prefix} Incident {timestamp}{suffix}"
        
        @staticmethod
        def generate_incident_description(incident_name: str) -> str:
            """Generate incident description based on name."""
            return f"Description for {incident_name}"
        
        @staticmethod
        def generate_search_terms() -> List[str]:
            """Generate various search terms for testing."""
            return [
                "test",
                "incident",
                "security",
                "urgent",
                "critical",
                "maintenance",
                "system",
                "error",
                "issue",
                "problem"
            ]
        
        @staticmethod
        def generate_pagination_scenarios() -> List[Dict[str, Any]]:
            """Generate pagination test scenarios."""
            return [
                {"page": 1, "limit": 1},
                {"page": 1, "limit": 5},
                {"page": 1, "limit": 10},
                {"page": 2, "limit": 5},
                {"page": 1, "limit": 100}
            ]
    
    return TestDataGenerator()


@pytest.fixture
def mock_incident_responses():
    """Fixture providing mock incident responses for testing."""
    return {
        "successful_create": {
            "id": 123,
            "name": "Test Incident",
            "description": "Test description",
            "category_id": 1,
            "priority": "medium",
            "status": "open",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        "successful_list": {
            "data": [
                {
                    "id": 1,
                    "name": "Incident 1",
                    "description": "Description 1",
                    "category_id": 1,
                    "priority": "high",
                    "status": "open"
                },
                {
                    "id": 2,
                    "name": "Incident 2",
                    "description": "Description 2",
                    "category_id": 2,
                    "priority": "medium",
                    "status": "in_progress"
                }
            ],
            "total": 2,
            "page": 1,
            "limit": 10,
            "total_pages": 1
        },
        "error_response": {
            "error": "Validation failed",
            "message": "Required field 'name' is missing",
            "code": "VALIDATION_ERROR"
        }
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "basic: mark test as basic functionality test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "negative: mark test as negative test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "detailed: mark test as detailed test"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test class or method names
        if "negative" in item.name or "invalid" in item.name or "error" in item.name:
            item.add_marker(pytest.mark.negative)
        
        if "performance" in item.name or "load" in item.name or "concurrent" in item.name:
            item.add_marker(pytest.mark.performance)
        
        if "smoke" in item.name or "basic" in item.name:
            item.add_marker(pytest.mark.smoke)
        
        if "regression" in item.name:
            item.add_marker(pytest.mark.regression)
