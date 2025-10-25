import pytest
import requests
from typing import Dict, Any
from config.config import BASE_URL, HEADERS, TIMEOUT

def test_delete_vehicle_success():
    """Test successful vehicle deletion"""
    # First create a vehicle to delete
    vehicle_data = {
        "name": "Vehicle to Delete",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "DELETE123"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Delete the vehicle
    response = requests.delete(f"{BASE_URL}/{vehicle_id}")
    assert response.status_code == 204  # No content

    # Verify vehicle is deleted by trying to get it
    get_response = requests.get(f"{BASE_URL}/{vehicle_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_vehicle():
    """Test deleting a vehicle that doesn't exist"""
    response = requests.delete(f"{BASE_URL}/999999")
    assert response.status_code == 404  # Not found

def test_delete_vehicle_in_use():
    """Test deleting a vehicle that is currently in use"""
    # First create a vehicle
    vehicle_data = {
        "name": "Active Vehicle",
        "type": "BUS",
        "capacity": 50,
        "status": "IN_ROUTE",  # Vehicle is currently in use
        "registration_number": "INUSE123"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Try to delete the vehicle that is in use
    response = requests.delete(f"{BASE_URL}/{vehicle_id}")
    assert response.status_code == 409  # Conflict - cannot delete vehicle in use 