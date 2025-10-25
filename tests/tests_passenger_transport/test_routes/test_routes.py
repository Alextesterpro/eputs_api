import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_route():
    """Test creating a new route"""
    url = f"{BASE_URL}/api/v1/routes"
    data = {
        "name": "Test Route",
        "start_station": "Station A",
        "end_station": "Station B",
        "stops": ["Station A", "Station C", "Station B"],
        "status": "active"
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]

def test_get_route():
    """Test getting a route by ID"""
    # First create a route
    url = f"{BASE_URL}/api/v1/routes"
    data = {
        "name": "Test Route",
        "start_station": "Station A",
        "end_station": "Station B",
        "stops": ["Station A", "Station C", "Station B"],
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    route_id = create_response.json()["id"]

    # Then get the route
    get_url = f"{BASE_URL}/api/v1/routes/{route_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["id"] == route_id

def test_update_route():
    """Test updating a route"""
    # First create a route
    url = f"{BASE_URL}/api/v1/routes"
    data = {
        "name": "Test Route",
        "start_station": "Station A",
        "end_station": "Station B",
        "stops": ["Station A", "Station C", "Station B"],
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    route_id = create_response.json()["id"]

    # Then update the route
    update_url = f"{BASE_URL}/api/v1/routes/{route_id}"
    update_data = {
        "name": "Updated Route",
        "start_station": "Station X",
        "end_station": "Station Y",
        "stops": ["Station X", "Station Z", "Station Y"],
        "status": "inactive"
    }
    response = requests.put(update_url, json=update_data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["name"] == update_data["name"]

def test_delete_route():
    """Test deleting a route"""
    # First create a route
    url = f"{BASE_URL}/api/v1/routes"
    data = {
        "name": "Test Route",
        "start_station": "Station A",
        "end_station": "Station B",
        "stops": ["Station A", "Station C", "Station B"],
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    route_id = create_response.json()["id"]

    # Then delete the route
    delete_url = f"{BASE_URL}/api/v1/routes/{route_id}"
    response = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 204

    # Verify the route is deleted
    get_url = f"{BASE_URL}/api/v1/routes/{route_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404 