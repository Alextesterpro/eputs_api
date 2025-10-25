import pytest
import requests
from config.config import BASE_URL, HEADERS, TIMEOUT

def test_update_vehicle():
    # Тестовые данные
    vehicle_id = 2313020
    test_data = {
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

    # Отправляем PUT запрос
    response = requests.put(
        f"{BASE_URL}/{vehicle_id}",
        headers=HEADERS,
        json=test_data,
        timeout=TIMEOUT
    )

    # Проверяем статус код
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Проверяем структуру ответа
    response_data = response.json()
    assert "success" in response_data, "Response should contain 'success' field"
    assert response_data["success"] is True, "Success should be True"
    assert "data" in response_data, "Response should contain 'data' field"

    # Проверяем данные в ответе
    vehicle_data = response_data["data"]
    assert vehicle_data["id"] == vehicle_id, f"Vehicle ID should be {vehicle_id}"
    assert vehicle_data["number"] == test_data["number"], "Vehicle number should match"
    assert vehicle_data["garage_number"] == test_data["garage_number"], "Garage number should match"
    assert vehicle_data["class_id"] == test_data["class_id"], "Class ID should match"
    assert vehicle_data["model_id"] == test_data["model_id"], "Model ID should match"
    assert vehicle_data["category_id"] == test_data["category_id"], "Category ID should match"
    assert vehicle_data["organization_id"] == test_data["organization_id"], "Organization ID should match"

    # Проверяем характеристики
    characteristics = vehicle_data["characteristics"]
    for key, value in test_data["characteristics"].items():
        assert characteristics[key] == value, f"Characteristic {key} should match" 