from tests_microservices.utils.api import TransportAPI

def test_update_nonexistent_station():
    update_data = {"name": "Несуществующая остановка"}
    response = TransportAPI.update_station(999999, update_data)
    assert response.status_code in (404, 422)

def test_delete_nonexistent_station():
    response = TransportAPI.delete_station(999999)
    assert response.status_code in (400, 404, 422)
    json_data = response.json()
    assert 'error_description' in json_data

def test_get_nonexistent_station():
    response = TransportAPI.get_station(999999)
    assert response.status_code in (400, 404, 422)
    json_data = response.json()
    assert 'error_description' in json_data 