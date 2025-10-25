from tests.tests_microservices.utils.api import TransportAPI

def test_list_routes():
    """Тест получения списка маршрутов"""
    response = TransportAPI.get_routes(page=1, limit=5)
    assert response.status_code == 200
    assert isinstance(response.json().get('data'), list) 