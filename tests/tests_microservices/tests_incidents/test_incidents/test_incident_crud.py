"""
Comprehensive CRUD tests for Incidents API.
Based on Postman collection with proper POM and assertions.
"""

import pytest
from typing import Dict, Any, Optional

from tests_microservices.utils.incidents.incidents_api import IncidentsAPI
from tests_microservices.utils.incidents.incident_schemas import (
    IncidentData,
    IncidentTestData,
    IncidentAssertions,
    IncidentValidators
)


@pytest.mark.basic
class TestIncidentCRUD:
    """Comprehensive CRUD tests for incidents API."""

    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        """Setup and cleanup for each test."""
        self.created_incident_id: Optional[int] = None
        yield
        # Cleanup: delete created incident if it exists
        if self.created_incident_id:
            try:
                IncidentsAPI.delete_incident(self.created_incident_id)
            except Exception:
                pass  # Ignore cleanup errors

    def test_create_incident_success(self):
        """Test successful incident creation."""
        # Arrange
        incident_data = IncidentTestData.create_valid_incident()
        
        # Act
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        
        # Assert
        created_incident = IncidentAssertions.assert_incident_created(response, incident_data)
        self.created_incident_id = created_incident["id"]
        
        # Additional validations
        assert created_incident["id"] is not None, "Incident ID should be assigned"
        assert created_incident["created_at"] is not None, "Created timestamp should be set"

    def test_create_incident_minimal_data(self):
        """Test incident creation with minimal required data."""
        # Arrange
        incident_data = IncidentTestData.create_minimal_incident()
        
        # Act
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        
        # Assert
        created_incident = IncidentAssertions.assert_incident_created(response, incident_data)
        self.created_incident_id = created_incident["id"]

    def test_create_incident_all_fields(self):
        """Test incident creation with all possible fields."""
        # Arrange
        incident_data = IncidentTestData.create_incident_with_all_fields()
        
        # Act
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        
        # Assert
        created_incident = IncidentAssertions.assert_incident_created(response, incident_data)
        self.created_incident_id = created_incident["id"]
        
        # Validate all fields
        assert created_incident["priority"] == incident_data.priority
        assert created_incident["status"] == incident_data.status

    def test_get_incident_success(self):
        """Test successful incident retrieval."""
        # Arrange - create incident first
        incident_data = IncidentTestData.create_valid_incident()
        create_response = IncidentsAPI.create_incident(incident_data.to_dict())
        assert create_response.status_code in [200, 201]
        created_incident = create_response.json()
        incident_id = created_incident["id"]
        self.created_incident_id = incident_id
        
        # Act
        response = IncidentsAPI.get_incident(incident_id)
        
        # Assert
        retrieved_incident = IncidentAssertions.assert_incident_retrieved(response, incident_id)
        
        # Validate data consistency
        assert retrieved_incident["name"] == incident_data.name
        assert retrieved_incident["description"] == incident_data.description
        assert retrieved_incident["category_id"] == incident_data.category_id

    def test_get_incident_not_found(self):
        """Test incident retrieval with non-existent ID."""
        # Arrange
        non_existent_id = 99999999
        
        # Act
        response = IncidentsAPI.get_incident(non_existent_id)
        
        # Assert
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"

    def test_update_incident_success(self):
        """Test successful incident update."""
        # Arrange - create incident first
        incident_data = IncidentTestData.create_valid_incident()
        create_response = IncidentsAPI.create_incident(incident_data.to_dict())
        assert create_response.status_code in [200, 201]
        created_incident = create_response.json()
        incident_id = created_incident["id"]
        self.created_incident_id = incident_id
        
        # Prepare update data
        updated_data = IncidentData(
            id=incident_id,
            name="Updated Incident Name",
            description="Updated description",
            category_id=1,
            priority="medium",
            status="in_progress"
        )
        
        # Act
        response = IncidentsAPI.update_incident(incident_id, updated_data.to_dict())
        
        # Assert
        updated_incident = IncidentAssertions.assert_incident_updated(response, updated_data)
        
        # Validate updated fields
        assert updated_incident["name"] == "Updated Incident Name"
        assert updated_incident["description"] == "Updated description"
        assert updated_incident["priority"] == "medium"
        assert updated_incident["status"] == "in_progress"

    def test_update_incident_partial(self):
        """Test partial incident update (only name)."""
        # Arrange - create incident first
        incident_data = IncidentTestData.create_valid_incident()
        create_response = IncidentsAPI.create_incident(incident_data.to_dict())
        assert create_response.status_code in [200, 201]
        created_incident = create_response.json()
        incident_id = created_incident["id"]
        self.created_incident_id = incident_id
        
        # Prepare partial update
        partial_update = {"name": "Partially Updated Name"}
        
        # Act
        response = IncidentsAPI.update_incident(incident_id, partial_update)
        
        # Assert
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}: {response.text}"
        
        # Verify only name was updated
        updated_incident = response.json()
        assert updated_incident["name"] == "Partially Updated Name"
        assert updated_incident["description"] == incident_data.description  # Should remain unchanged

    def test_update_incident_not_found(self):
        """Test incident update with non-existent ID."""
        # Arrange
        non_existent_id = 99999999
        update_data = {"name": "Updated Name"}
        
        # Act
        response = IncidentsAPI.update_incident(non_existent_id, update_data)
        
        # Assert
        assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"

    def test_delete_incident_success(self):
        """Test successful incident deletion."""
        # Arrange - create incident first
        incident_data = IncidentTestData.create_valid_incident()
        create_response = IncidentsAPI.create_incident(incident_data.to_dict())
        assert create_response.status_code in [200, 201]
        created_incident = create_response.json()
        incident_id = created_incident["id"]
        
        # Act
        response = IncidentsAPI.delete_incident(incident_id)
        
        # Assert
        IncidentAssertions.assert_incident_deleted(response)
        
        # Verify incident is actually deleted
        get_response = IncidentsAPI.get_incident(incident_id)
        assert get_response.status_code == 404, "Incident should be deleted"

    def test_delete_incident_not_found(self):
        """Test incident deletion with non-existent ID."""
        # Arrange
        non_existent_id = 99999999
        
        # Act
        response = IncidentsAPI.delete_incident(non_existent_id)
        
        # Assert
        assert response.status_code in [404, 200, 204], f"Expected 404/200/204, got {response.status_code}: {response.text}"

    def test_crud_workflow(self):
        """Test complete CRUD workflow in sequence."""
        # 1. Create incident
        incident_data = IncidentTestData.create_valid_incident()
        create_response = IncidentsAPI.create_incident(incident_data.to_dict())
        assert create_response.status_code in [200, 201]
        created_incident = create_response.json()
        incident_id = created_incident["id"]
        self.created_incident_id = incident_id
        
        # 2. Read incident
        get_response = IncidentsAPI.get_incident(incident_id)
        assert get_response.status_code == 200
        retrieved_incident = get_response.json()
        assert retrieved_incident["id"] == incident_id
        
        # 3. Update incident
        updated_data = IncidentData(
            id=incident_id,
            name="Workflow Updated Name",
            description="Workflow updated description",
            category_id=1,
            priority="low",
            status="closed"
        )
        update_response = IncidentsAPI.update_incident(incident_id, updated_data.to_dict())
        assert update_response.status_code in [200, 201]
        
        # 4. Verify update
        get_updated_response = IncidentsAPI.get_incident(incident_id)
        assert get_updated_response.status_code == 200
        updated_incident = get_updated_response.json()
        assert updated_incident["name"] == "Workflow Updated Name"
        assert updated_incident["status"] == "closed"
        
        # 5. Delete incident
        delete_response = IncidentsAPI.delete_incident(incident_id)
        assert delete_response.status_code in [200, 204]
        
        # 6. Verify deletion
        final_get_response = IncidentsAPI.get_incident(incident_id)
        assert final_get_response.status_code == 404
        
        # Mark as cleaned up
        self.created_incident_id = None


@pytest.mark.smoke
class TestIncidentSmoke:
    """Smoke tests for critical incident functionality."""

    def test_incident_api_connectivity(self):
        """Test basic API connectivity."""
        # Test with a simple list request
        list_payload = {"page": 1, "limit": 1, "is_simple": True}
        response = IncidentsAPI.list_incidents(list_payload)
        
        # Should not be 401 (unauthorized) or 500 (server error)
        assert response.status_code not in [401, 500], f"API connectivity issue: {response.status_code} - {response.text}"
        
        # Should be either 200 (success) or 404 (no data)
        assert response.status_code in [200, 404], f"Unexpected status: {response.status_code} - {response.text}"

    def test_incident_authentication(self):
        """Test authentication is working."""
        # Try to create an incident (requires auth)
        incident_data = IncidentTestData.create_minimal_incident()
        response = IncidentsAPI.create_incident(incident_data.to_dict())
        
        # Should not be 401 (unauthorized)
        assert response.status_code != 401, "Authentication failed - check token"
        
        # If successful, clean up
        if response.status_code in [200, 201]:
            created_incident = response.json()
            incident_id = created_incident.get("id")
            if incident_id:
                try:
                    IncidentsAPI.delete_incident(incident_id)
                except Exception:
                    pass  # Ignore cleanup errors
