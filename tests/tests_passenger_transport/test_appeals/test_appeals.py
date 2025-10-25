import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_create_appeal():
    """Test creating a new appeal"""
    url = f"{BASE_URL}/api/v1/appeals"
    data = {
        "title": "Test Appeal",
        "description": "This is a test appeal",
        "status": "open"
    }
    response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]

def test_get_appeal():
    """Test getting an appeal by ID"""
    # First create an appeal
    url = f"{BASE_URL}/api/v1/appeals"
    data = {
        "title": "Test Appeal",
        "description": "This is a test appeal",
        "status": "open"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    appeal_id = create_response.json()["id"]

    # Then get the appeal
    get_url = f"{BASE_URL}/api/v1/appeals/{appeal_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["id"] == appeal_id

def test_update_appeal():
    """Test updating an appeal"""
    # First create an appeal
    url = f"{BASE_URL}/api/v1/appeals"
    data = {
        "title": "Test Appeal",
        "description": "This is a test appeal",
        "status": "open"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    appeal_id = create_response.json()["id"]

    # Then update the appeal
    update_url = f"{BASE_URL}/api/v1/appeals/{appeal_id}"
    update_data = {
        "title": "Updated Appeal",
        "description": "This is an updated test appeal",
        "status": "closed"
    }
    response = requests.put(update_url, json=update_data, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["title"] == update_data["title"]

def test_delete_appeal():
    """Test deleting an appeal"""
    # First create an appeal
    url = f"{BASE_URL}/api/v1/appeals"
    data = {
        "title": "Test Appeal",
        "description": "This is a test appeal",
        "status": "open"
    }
    create_response = requests.post(url, json=data, headers=HEADERS, timeout=TIMEOUT)
    appeal_id = create_response.json()["id"]

    # Then delete the appeal
    delete_url = f"{BASE_URL}/api/v1/appeals/{appeal_id}"
    response = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 204

    # Verify the appeal is deleted
    get_url = f"{BASE_URL}/api/v1/appeals/{appeal_id}"
    response = requests.get(get_url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 404 