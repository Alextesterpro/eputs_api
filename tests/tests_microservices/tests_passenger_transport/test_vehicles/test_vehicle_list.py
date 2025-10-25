import pytest
import requests
from typing import Dict, Any
from config.config import BASE_URL, HEADERS, TIMEOUT

def test_list_vehicles_success():
    """Test successful vehicle listing"""
    # First create a test vehicle
    vehicle_data = {
        "name": "List Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "LIST001"
    }
    create_response = requests.post(BASE_URL, json=vehicle_data)
    assert create_response.status_code == 201

    # Get list of vehicles
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    vehicles = response.json()
    
    # Verify response structure
    assert isinstance(vehicles, list)
    if vehicles:
        vehicle = vehicles[0]
        assert "id" in vehicle
        assert "name" in vehicle
        assert "type" in vehicle
        assert "capacity" in vehicle
        assert "status" in vehicle
        assert "registration_number" in vehicle

def test_list_vehicles_with_filters():
    """Test vehicle listing with filters"""
    # Create test vehicles with different types and statuses
    bus_data = {
        "name": "Filter Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "ACTIVE",
        "registration_number": "FILTER001"
    }
    minibus_data = {
        "name": "Filter Test Minibus",
        "type": "MINIBUS",
        "capacity": 20,
        "status": "MAINTENANCE",
        "registration_number": "FILTER002"
    }
    
    requests.post(BASE_URL, json=bus_data)
    requests.post(BASE_URL, json=minibus_data)

    # Test type filter
    response = requests.get(f"{BASE_URL}?type=BUS")
    assert response.status_code == 200
    buses = response.json()
    assert all(vehicle["type"] == "BUS" for vehicle in buses)

    # Test status filter
    response = requests.get(f"{BASE_URL}?status=MAINTENANCE")
    assert response.status_code == 200
    maintenance_vehicles = response.json()
    assert all(vehicle["status"] == "MAINTENANCE" for vehicle in maintenance_vehicles)

def test_list_vehicles_pagination():
    """Test vehicle listing with pagination"""
    # Create multiple test vehicles
    for i in range(5):
        vehicle_data = {
            "name": f"Pagination Test Bus {i}",
            "type": "BUS",
            "capacity": 50,
            "status": "ACTIVE",
            "registration_number": f"PAGE00{i}"
        }
        requests.post(BASE_URL, json=vehicle_data)

    # Test with page size
    response = requests.get(f"{BASE_URL}?page=1&size=3")
    assert response.status_code == 200
    vehicles = response.json()
    assert len(vehicles) <= 3  # Should not exceed page size

    # Test second page
    response = requests.get(f"{BASE_URL}?page=2&size=3")
    assert response.status_code == 200
    vehicles = response.json()
    assert isinstance(vehicles, list)  # Should return a list even if empty

def test_list_vehicles_empty():
    """Test vehicle listing when no vehicles match criteria"""
    # Try to get vehicles with non-existent type
    response = requests.get(f"{BASE_URL}?type=NONEXISTENT")
    assert response.status_code == 200
    vehicles = response.json()
    assert isinstance(vehicles, list)
    assert len(vehicles) == 0  # Should return empty list 