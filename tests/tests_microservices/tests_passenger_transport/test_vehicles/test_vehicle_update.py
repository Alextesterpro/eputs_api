import pytest
import requests
from typing import Dict, Any
from config.config import BASE_URL, HEADERS, TIMEOUT

def test_update_vehicle_success():
    """Test successful vehicle update"""
    # First create a vehicle to update
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "ABC123"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Update the vehicle
    update_data = {
        "name": "Updated Bus",
        "capacity": 60,
        "status": "MAINTENANCE"
    }
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=update_data)
    assert response.status_code == 200
    updated_vehicle = response.json()
    assert updated_vehicle["name"] == update_data["name"]
    assert updated_vehicle["capacity"] == update_data["capacity"]
    assert updated_vehicle["status"] == update_data["status"]

def test_update_vehicle_invalid_data():
    """Test vehicle update with invalid data"""
    # First create a vehicle
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "ABC124"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Try to update with invalid data
    invalid_data = {
        "capacity": -10,  # Invalid capacity
        "status": "INVALID_STATUS"  # Invalid status
    }
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=invalid_data)
    assert response.status_code == 422  # Validation error

def test_update_nonexistent_vehicle():
    """Test updating a vehicle that doesn't exist"""
    update_data = {
        "name": "Nonexistent Bus",
        "capacity": 50
    }
    response = requests.put(f"{BASE_URL}/999999", json=update_data)
    assert response.status_code == 404  # Not found 