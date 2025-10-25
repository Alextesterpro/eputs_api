import pytest
from tests.tests_microservices.utils.api import TransportAPI

ROUTE_DATA = {
    "name": "Тестовый маршрут",
    "road": {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [
                [102, 0],
                [103, 1],
                [104, 0],
                [105, 1]
            ]
        }
    },
    "num": "101",
    "duration": 60,
    "category_id": 1,
    "group_num": "101",
    "group_order": 1
}

def test_update_route():
    """Тест обновления маршрута"""
    data = ROUTE_DATA.copy()
    create_resp = TransportAPI.create_route(**data)
    assert create_resp.status_code in (200, 201)
    route_id = create_resp.json().get('data', {}).get('id')
    assert route_id

    # Обновляем маршрут
    update_data = ROUTE_DATA.copy()
    update_data['name'] = "Обновлённый маршрут"
    update_resp = TransportAPI.update_route(route_id, update_data)
    assert update_resp.status_code == 200
    assert update_resp.json().get('data', {}).get('name') == "Обновлённый маршрут" 