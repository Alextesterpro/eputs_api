import pytest
import requests
from typing import Dict, Any
from config.config import BASE_URL, HEADERS, TIMEOUT

def test_create_vehicle_missing_required_fields():
    """Test vehicle creation with missing required fields"""
    incomplete_data = {
        "name": "Test Vehicle"
        # Missing type, capacity, status, registration_number
    }
    response = requests.post(BASE_URL, json=incomplete_data)
    assert response.status_code == 422

def test_create_vehicle_invalid_type():
    """Test vehicle creation with invalid vehicle type"""
    invalid_data = {
        "name": "Test Vehicle",
        "type": "ROCKET",  # Invalid type
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "TEST123"
    }
    response = requests.post(BASE_URL, json=invalid_data)
    assert response.status_code == 422
    error_data = response.json()
    assert "type" in str(error_data["detail"]).lower()

def test_create_vehicle_invalid_capacity():
    """Test vehicle creation with invalid capacity values"""
    # Test with negative capacity
    negative_capacity = {
        "name": "Test Vehicle",
        "type": "BUS",
        "capacity": -10,
        "status": "ACTIVE",
        "registration_number": "TEST124"
    }
    response = requests.post(BASE_URL, json=negative_capacity)
    assert response.status_code == 422

    # Test with zero capacity
    zero_capacity = {
        "name": "Test Vehicle",
        "type": "BUS",
        "capacity": 0,
        "status": "ACTIVE",
        "registration_number": "TEST125"
    }
    response = requests.post(BASE_URL, json=zero_capacity)
    assert response.status_code == 422

def test_create_vehicle_invalid_status():
    """Test vehicle creation with invalid status"""
    invalid_data = {
        "name": "Test Vehicle",
        "type": "BUS",
        "capacity": 50,
        "status": "FLYING",  # Invalid status
        "registration_number": "TEST126"
    }
    response = requests.post(BASE_URL, json=invalid_data)
    assert response.status_code == 422
    error_data = response.json()
    assert "status" in str(error_data["detail"]).lower()

def test_create_vehicle_invalid_registration_format():
    """Test vehicle creation with invalid registration number format"""
    invalid_data = {
        "name": "Test Vehicle",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "!@#$%^"  # Invalid format
    }
    response = requests.post(BASE_URL, json=invalid_data)
    assert response.status_code == 422
    error_data = response.json()
    assert "registration_number" in str(error_data["detail"]).lower() 