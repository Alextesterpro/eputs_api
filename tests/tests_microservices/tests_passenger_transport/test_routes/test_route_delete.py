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

def test_delete_route():
    """Тест удаления маршрута по ID"""
    data = ROUTE_DATA.copy()
    create_resp = TransportAPI.create_route(**data)
    assert create_resp.status_code in (200, 201)
    route_id = create_resp.json().get('data', {}).get('id')
    assert route_id

    # Удаляем маршрут
    delete_resp = TransportAPI.delete_route(route_id=route_id, headers={"project": "98_spb"})
    assert delete_resp.status_code == 200
    # Можно добавить проверку, что маршрут реально удалён (например, попытаться получить его и получить 404)
    # get_resp = TransportAPI.get_route(route_id)
    # assert get_resp.status_code == 404 