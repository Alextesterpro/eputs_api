import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_transport_invalid_data():
    """Test creating a transport with invalid data"""
    url = f"{BASE_URL}/api/v1/transport"
    data = {
        "type": "invalid_type",  # Invalid transport type
        "number": "",  # Empty number
        "capacity": -1,  # Invalid capacity
        "status": "invalid_status"  # Invalid status
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 400

def test_get_nonexistent_transport():
    """Test getting a non-existent transport"""
    url = f"{BASE_URL}/api/v1/transport/999999"  # Non-existent ID
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_update_nonexistent_transport():
    """Test updating a non-existent transport"""
    url = f"{BASE_URL}/api/v1/transport/999999"  # Non-existent ID
    data = {
        "type": "bus",
        "number": "456",
        "capacity": 60,
        "status": "maintenance"
    }
    response = requests.put(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_delete_nonexistent_transport():
    """Test deleting a non-existent transport"""
    url = f"{BASE_URL}/api/v1/transport/999999"  # Non-existent ID
    response = requests.delete(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_create_transport_missing_required_fields():
    """Test creating a transport with missing required fields"""
    url = f"{BASE_URL}/api/v1/transport"
    data = {
        "number": "123"  # Missing type, capacity, and status
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 400 