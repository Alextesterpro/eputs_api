import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_station():
    """Test creating a new station"""
    url = f"{BASE_URL}/api/v1/stations"
    data = {
        "name": "Test Station",
        "location": "Test Location",
        "capacity": 100,
        "status": "active"
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]

def test_get_station():
    """Test getting a station by ID"""
    # First create a station
    url = f"{BASE_URL}/api/v1/stations"
    data = {
        "name": "Test Station",
        "location": "Test Location",
        "capacity": 100,
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    station_id = create_response.json()["id"]

    # Then get the station
    get_url = f"{BASE_URL}/api/v1/stations/{station_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["id"] == station_id

def test_update_station():
    """Test updating a station"""
    # First create a station
    url = f"{BASE_URL}/api/v1/stations"
    data = {
        "name": "Test Station",
        "location": "Test Location",
        "capacity": 100,
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    station_id = create_response.json()["id"]

    # Then update the station
    update_url = f"{BASE_URL}/api/v1/stations/{station_id}"
    update_data = {
        "name": "Updated Station",
        "location": "Updated Location",
        "capacity": 150,
        "status": "maintenance"
    }
    response = requests.put(update_url, json=update_data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_delete_station():
    """Test deleting a station"""
    # First create a station
    url = f"{BASE_URL}/api/v1/stations"
    data = {
        "name": "Test Station",
        "location": "Test Location",
        "capacity": 100,
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    station_id = create_response.json()["id"]

    # Then delete the station
    delete_url = f"{BASE_URL}/api/v1/stations/{station_id}"
    response = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 204

    # Verify the station is deleted
    get_url = f"{BASE_URL}/api/v1/stations/{station_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404 