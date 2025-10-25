import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_appeal_invalid_data():
    """Test creating an appeal with invalid data"""
    url = f"{BASE_URL}/api/v1/appeals"
    data = {
        "title": "",  # Empty title
        "description": "This is a test appeal",
        "status": "invalid_status"  # Invalid status
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 400

def test_get_nonexistent_appeal():
    """Test getting a non-existent appeal"""
    url = f"{BASE_URL}/api/v1/appeals/999999"  # Non-existent ID
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_update_nonexistent_appeal():
    """Test updating a non-existent appeal"""
    url = f"{BASE_URL}/api/v1/appeals/999999"  # Non-existent ID
    data = {
        "title": "Updated Appeal",
        "description": "This is an updated test appeal",
        "status": "closed"
    }
    response = requests.put(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_delete_nonexistent_appeal():
    """Test deleting a non-existent appeal"""
    url = f"{BASE_URL}/api/v1/appeals/999999"  # Non-existent ID
    response = requests.delete(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_create_appeal_missing_required_fields():
    """Test creating an appeal with missing required fields"""
    url = f"{BASE_URL}/api/v1/appeals"
    data = {
        "description": "This is a test appeal"  # Missing title and status
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 400 