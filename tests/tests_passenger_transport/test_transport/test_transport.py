import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_transport():
    """Test creating a new transport"""
    url = f"{BASE_URL}/api/v1/transport"
    data = {
        "type": "bus",
        "number": "123",
        "capacity": 50,
        "status": "active"
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 201
    assert response.json()["number"] == data["number"]

def test_get_transport():
    """Test getting a transport by ID"""
    # First create a transport
    url = f"{BASE_URL}/api/v1/transport"
    data = {
        "type": "bus",
        "number": "123",
        "capacity": 50,
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    transport_id = create_response.json()["id"]

    # Then get the transport
    get_url = f"{BASE_URL}/api/v1/transport/{transport_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["id"] == transport_id

def test_update_transport():
    """Test updating a transport"""
    # First create a transport
    url = f"{BASE_URL}/api/v1/transport"
    data = {
        "type": "bus",
        "number": "123",
        "capacity": 50,
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    transport_id = create_response.json()["id"]

    # Then update the transport
    update_url = f"{BASE_URL}/api/v1/transport/{transport_id}"
    update_data = {
        "type": "bus",
        "number": "456",
        "capacity": 60,
        "status": "maintenance"
    }
    response = requests.put(update_url, json=update_data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["number"] == update_data["number"]

def test_delete_transport():
    """Test deleting a transport"""
    # First create a transport
    url = f"{BASE_URL}/api/v1/transport"
    data = {
        "type": "bus",
        "number": "123",
        "capacity": 50,
        "status": "active"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    transport_id = create_response.json()["id"]

    # Then delete the transport
    delete_url = f"{BASE_URL}/api/v1/transport/{transport_id}"
    response = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 204

    # Verify the transport is deleted
    get_url = f"{BASE_URL}/api/v1/transport/{transport_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404 