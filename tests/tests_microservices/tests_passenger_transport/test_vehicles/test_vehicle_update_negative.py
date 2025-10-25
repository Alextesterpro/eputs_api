import pytest
import requests
from typing import Dict, Any
from config.config import BASE_URL, HEADERS, TIMEOUT

def test_update_vehicle_invalid_status_transition():
    """Test invalid vehicle status transitions"""
    # First create a vehicle
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "IN_ROUTE",
        "registration_number": "TEST127"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Try to update status from IN_ROUTE to DELETED
    invalid_update = {
        "status": "DELETED"
    }
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=invalid_update)
    assert response.status_code == 422

def test_update_vehicle_invalid_capacity():
    """Test updating vehicle with invalid capacity"""
    # First create a vehicle
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "TEST128"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Try to update with invalid capacity
    invalid_update = {
        "capacity": -5
    }
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=invalid_update)
    assert response.status_code == 422

def test_update_vehicle_empty_name():
    """Test updating vehicle with empty name"""
    # First create a vehicle
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "TEST129"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Try to update with empty name
    invalid_update = {
        "name": ""
    }
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=invalid_update)
    assert response.status_code == 422

def test_update_vehicle_immutable_fields():
    """Test updating immutable fields"""
    # First create a vehicle
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "TEST130"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201
    vehicle_id = create_response.json()["id"]

    # Try to update immutable fields
    invalid_update = {
        "type": "MINIBUS",  # Type should be immutable
        "registration_number": "NEW123"  # Registration number should be immutable
    }
    response = requests.put(f"{BASE_URL}/{vehicle_id}", json=invalid_update)
    assert response.status_code == 422 