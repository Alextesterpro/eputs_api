"""
Data models and schemas for incident API testing.
Based on Postman collection analysis.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class IncidentData:
    """Data model for incident creation and updates."""
    
    name: str
    description: str
    category_id: int
    priority: str = "medium"
    status: str = "open"
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        data = asdict(self)
        # Remove None values
        return {k: v for k, v in data.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IncidentData':
        """Create from dictionary (API response)."""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class IncidentListRequest:
    """Data model for incident list requests."""
    
    page: int = 1
    limit: int = 10
    is_simple: bool = True
    category_id: Optional[int] = None
    status: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class IncidentSearchRequest:
    """Data model for incident search requests."""
    
    page: int = 1
    limit: int = 10
    search: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class IncidentListResponse:
    """Data model for incident list responses."""
    
    data: List[Dict[str, Any]]
    total: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    total_pages: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IncidentListResponse':
        """Create from API response dictionary."""
        return cls(
            data=data.get("data", []),
            total=data.get("total"),
            page=data.get("page"),
            limit=data.get("limit"),
            total_pages=data.get("total_pages")
        )


class IncidentTestData:
    """Factory for creating test incident data."""
    
    @staticmethod
    def create_valid_incident() -> IncidentData:
        """Create a valid incident for testing."""
        return IncidentData(
            name="Test Incident",
            description="Test incident description",
            category_id=1,
            priority="high",
            status="open"
        )
    
    @staticmethod
    def create_minimal_incident() -> IncidentData:
        """Create minimal incident with required fields only."""
        return IncidentData(
            name="Minimal Test Incident",
            description="Minimal description",
            category_id=1
        )
    
    @staticmethod
    def create_incident_with_all_fields() -> IncidentData:
        """Create incident with all possible fields."""
        return IncidentData(
            name="Full Test Incident",
            description="Full test incident description with all fields",
            category_id=1,
            priority="medium",
            status="in_progress"
        )
    
    @staticmethod
    def create_invalid_incident() -> Dict[str, Any]:
        """Create invalid incident data for negative testing."""
        return {
            "name": "",  # Empty name should fail validation
            "description": "Test description",
            "category_id": "invalid",  # Wrong type
            "priority": "invalid_priority",  # Invalid enum value
            "status": "invalid_status"  # Invalid enum value
        }
    
    @staticmethod
    def create_search_request() -> IncidentSearchRequest:
        """Create search request for testing."""
        return IncidentSearchRequest(
            page=1,
            limit=5,
            search="test",
            category_id=1,
            status="open"
        )
    
    @staticmethod
    def create_list_request() -> IncidentListRequest:
        """Create list request for testing."""
        return IncidentListRequest(
            page=1,
            limit=10,
            is_simple=True
        )


class IncidentValidators:
    """Validators for incident API responses."""
    
    @staticmethod
    def validate_incident_response(response_data: Dict[str, Any]) -> bool:
        """Validate incident response structure."""
        required_fields = ["id", "name", "description", "category_id"]
        return all(field in response_data for field in required_fields)
    
    @staticmethod
    def validate_incident_list_response(response_data: Dict[str, Any]) -> bool:
        """Validate incident list response structure."""
        required_fields = ["data"]
        if not all(field in response_data for field in required_fields):
            return False
        
        # Validate data is a list
        if not isinstance(response_data["data"], list):
            return False
        
        # If there are items, validate their structure
        if response_data["data"]:
            return IncidentValidators.validate_incident_response(response_data["data"][0])
        
        return True
    
    @staticmethod
    def validate_error_response(response_data: Dict[str, Any]) -> bool:
        """Validate error response structure."""
        return "error" in response_data or "message" in response_data
    
    @staticmethod
    def validate_pagination(response_data: Dict[str, Any]) -> bool:
        """Validate pagination fields in list response."""
        pagination_fields = ["page", "limit", "total", "total_pages"]
        return any(field in response_data for field in pagination_fields)


class IncidentAssertions:
    """Helper class for incident API assertions."""
    
    @staticmethod
    def assert_incident_created(response, incident_data: IncidentData):
        """Assert incident was created successfully."""
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert IncidentValidators.validate_incident_response(data), "Invalid incident response structure"
        
        # Validate specific fields
        assert data["name"] == incident_data.name, f"Name mismatch: expected {incident_data.name}, got {data['name']}"
        assert data["description"] == incident_data.description, "Description mismatch"
        assert data["category_id"] == incident_data.category_id, "Category ID mismatch"
        
        return data
    
    @staticmethod
    def assert_incident_retrieved(response, expected_id: int):
        """Assert incident was retrieved successfully."""
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert IncidentValidators.validate_incident_response(data), "Invalid incident response structure"
        assert data["id"] == expected_id, f"ID mismatch: expected {expected_id}, got {data['id']}"
        
        return data
    
    @staticmethod
    def assert_incident_updated(response, incident_data: IncidentData):
        """Assert incident was updated successfully."""
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert IncidentValidators.validate_incident_response(data), "Invalid incident response structure"
        
        # Validate updated fields
        assert data["name"] == incident_data.name, "Name not updated"
        assert data["description"] == incident_data.description, "Description not updated"
        
        return data
    
    @staticmethod
    def assert_incident_deleted(response):
        """Assert incident was deleted successfully."""
        assert response.status_code in [200, 204], f"Expected 200/204, got {response.status_code}: {response.text}"
    
    @staticmethod
    def assert_incident_list(response, expected_count: Optional[int] = None):
        """Assert incident list was retrieved successfully."""
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert IncidentValidators.validate_incident_list_response(data), "Invalid list response structure"
        
        if expected_count is not None:
            assert len(data["data"]) == expected_count, f"Expected {expected_count} items, got {len(data['data'])}"
        
        return data
    
    @staticmethod
    def assert_incident_search(response, search_term: Optional[str] = None):
        """Assert incident search was successful."""
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert IncidentValidators.validate_incident_list_response(data), "Invalid search response structure"
        
        # If search term provided, validate results contain the term
        if search_term and data["data"]:
            for item in data["data"]:
                assert search_term.lower() in item.get("name", "").lower() or \
                       search_term.lower() in item.get("description", "").lower(), \
                       f"Search term '{search_term}' not found in results"
        
        return data
    
    @staticmethod
    def assert_error_response(response, expected_status: int, expected_message: Optional[str] = None):
        """Assert error response."""
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert IncidentValidators.validate_error_response(data), "Invalid error response structure"
        
        if expected_message:
            error_text = data.get("error", data.get("message", ""))
            assert expected_message.lower() in error_text.lower(), f"Expected message '{expected_message}' not found in '{error_text}'"
        
        return data
