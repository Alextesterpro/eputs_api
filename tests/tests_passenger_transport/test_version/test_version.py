import pytest
import requests
from config import BASE_URL, HEADERS, TIMEOUT

def test_get_version():
    """Test getting the API version"""
    url = f"{BASE_URL}/api/v1/version"
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    assert response.status_code == 200
    assert "version" in response.json()
    assert "build_date" in response.json()
    assert "commit_hash" in response.json() 