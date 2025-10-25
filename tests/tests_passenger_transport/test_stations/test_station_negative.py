import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_station_invalid_data():
    """Test creating a station with invalid data"""
    url = f"{BASE_URL}/api/v1/stations"
    data = {
        "name": "",  # Empty name
        "location": "Test Location",
        "capacity": -1,  # Invalid capacity
        "status": "invalid_status"  # Invalid status
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 400

def test_get_nonexistent_station():
    """Test getting a non-existent station"""
    url = f"{BASE_URL}/api/v1/stations/999999"  # Non-existent ID
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_update_nonexistent_station():
    """Test updating a non-existent station"""
    url = f"{BASE_URL}/api/v1/stations/999999"  # Non-existent ID
    data = {
        "name": "Updated Station",
        "location": "Updated Location",
        "capacity": 150,
        "status": "maintenance"
    }
    response = requests.put(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_delete_nonexistent_station():
    """Test deleting a non-existent station"""
    url = f"{BASE_URL}/api/v1/stations/999999"  # Non-existent ID
    response = requests.delete(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404

def test_create_station_missing_required_fields():
    """Test creating a station with missing required fields"""
    url = f"{BASE_URL}/api/v1/stations"
    data = {
        "location": "Test Location"  # Missing name, capacity, and status
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 400 