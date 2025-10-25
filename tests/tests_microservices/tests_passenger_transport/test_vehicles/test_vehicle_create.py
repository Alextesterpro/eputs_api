import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT
from datetime import datetime
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_create_vehicle_success():
    """Test successful vehicle creation"""
    try:
        response = requests.post(
            f"{BASE_URL}/vehicles",
            json={
                "number": "A222AA197RUS",
                "garage_number": "884",
                "class_id": 2,
                "model_id": 61,
                "category_id": 1,
                "organization_id": 4,
                "characteristics": {
                    "wc": "2",
                    "uid": "66",
                    "vin": "656",
                    "name": "Имя",
                    "model": "3554",
                    "speed": "14",
                    "carnum": "434",
                    "capacity": "4",
                    "low_floor": "1",
                    "is_invalid": "0",
                    "count_seats": "5",
                    "curb_weight": "4",
                    "useful_area": "10",
                    "conditioning": "4535",
                    "bicycle_racks": "1",
                    "overall_width": "55",
                    "overall_height": "29",
                    "overall_length": "44",
                    "places_for_strollers": "1"
                },
                "egts_receiver_id": 0
            },
            headers=HEADERS,
            timeout=TIMEOUT
        )
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response text: {response.text}")
        assert response.status_code == 201
        data = response.json()
        assert data["number"] == "A222AA197RUS"
        assert data["garage_number"] == "884"
        assert "id" in data
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

def test_create_vehicle_with_minibus_type():
    """Test vehicle creation with MINIBUS type"""
    try:
        vehicle_data = {
            "number": "B333BB197RUS",
            "garage_number": "885",
            "class_id": 2,
            "model_id": 61,
            "category_id": 1,
            "organization_id": 4,
            "characteristics": {
                "wc": "2",
                "uid": "67",
                "vin": "657",
                "name": "Микроавтобус",
                "model": "3554",
                "speed": "14",
                "carnum": "435",
                "capacity": "4",
                "low_floor": "1",
                "is_invalid": "0",
                "count_seats": "5",
                "curb_weight": "4",
                "useful_area": "10",
                "conditioning": "4535",
                "bicycle_racks": "1",
                "overall_width": "55",
                "overall_height": "29",
                "overall_length": "44",
                "places_for_strollers": "1"
            },
            "egts_receiver_id": 0
        }
        response = requests.post(f"{BASE_URL}/vehicles", json=vehicle_data, headers=HEADERS, timeout=TIMEOUT)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response text: {response.text}")
        assert response.status_code == 201
        created_vehicle = response.json()
        assert created_vehicle["number"] == "B333BB197RUS"
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

def test_create_vehicle_with_maintenance_status():
    """Test vehicle creation with MAINTENANCE status"""
    vehicle_data = {
        "name": "Test Bus",
        "type": "BUS",
        "capacity": 50,
        "status": "MAINTENANCE",
        "registration_number": "TEST003"
    }
    response = requests.post(f"{BASE_URL}/vehicles", json=vehicle_data, headers=HEADERS)
    assert response.status_code == 201
    created_vehicle = response.json()
    assert created_vehicle["status"] == "MAINTENANCE"

def test_create_vehicle_with_max_capacity():
    """Test vehicle creation with maximum allowed capacity"""
    vehicle_data = {
        "name": "Large Bus",
        "type": "BUS",
        "capacity": 100,  # Maximum capacity
        "status": "ACTIVE",
        "registration_number": "TEST004"
    }
    response = requests.post(f"{BASE_URL}/vehicles", json=vehicle_data, headers=HEADERS)
    assert response.status_code == 201
    created_vehicle = response.json()
    assert created_vehicle["capacity"] == 100

def test_create_vehicle_invalid_data():
    """Test vehicle creation with invalid data"""
    try:
        invalid_data = {
            "number": "",  # Empty number
            "garage_number": "",
            "class_id": -1,  # Invalid class_id
            "model_id": -1,  # Invalid model_id
            "category_id": -1,  # Invalid category_id
            "organization_id": -1,  # Invalid organization_id
            "characteristics": {
                "capacity": "-1"  # Invalid capacity
            }
        }
        
        response = requests.post(f"{BASE_URL}/vehicles", json=invalid_data, headers=HEADERS, timeout=TIMEOUT)
        logger.debug(f"Response status code: {response.status_code}")
        logger.debug(f"Response text: {response.text}")
        assert response.status_code == 422  # Assuming FastAPI validation error
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

def test_create_vehicle_duplicate_number():
    """Test vehicle creation with duplicate number"""
    try:
        # First create a vehicle
        vehicle_data = {
            "number": "C444CC197RUS",
            "garage_number": "886",
            "class_id": 2,
            "model_id": 61,
            "category_id": 1,
            "organization_id": 4,
            "characteristics": {
                "wc": "2",
                "uid": "68",
                "vin": "658",
                "name": "Дубликат",
                "model": "3554",
                "speed": "14",
                "carnum": "436",
                "capacity": "4",
                "low_floor": "1",
                "is_invalid": "0",
                "count_seats": "5",
                "curb_weight": "4",
                "useful_area": "10",
                "conditioning": "4535",
                "bicycle_racks": "1",
                "overall_width": "55",
                "overall_height": "29",
                "overall_length": "44",
                "places_for_strollers": "1"
            },
            "egts_receiver_id": 0
        }
        
        # Create first vehicle
        response = requests.post(f"{BASE_URL}/vehicles", json=vehicle_data, headers=HEADERS, timeout=TIMEOUT)
        logger.debug(f"First request response status code: {response.status_code}")
        logger.debug(f"First request response text: {response.text}")
        assert response.status_code == 201
        
        # Try to create another vehicle with same number
        response = requests.post(f"{BASE_URL}/vehicles", json=vehicle_data, headers=HEADERS, timeout=TIMEOUT)
        logger.debug(f"Second request response status code: {response.status_code}")
        logger.debug(f"Second request response text: {response.text}")
        assert response.status_code == 409  # Conflict status code
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise 