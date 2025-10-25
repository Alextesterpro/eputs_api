import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from tests_microservices.utils.api import TransportAPI

STATION_DATA = {
    "name": "Остановка 1",
    "direction": "",
    "comment": "",
    "attribute": 1,
    "is_smart": False,
    "type_list": [
        {
            "id": 2,
            "name": "Троллейбус",
            "slug": "Trolleybus",
            "color": "#4a90e2",
            "image": "",
            "image_with_work_order": "",
            "station_name": "Троллейбусная",
            "color_not_in_registry": "#77ace9"
        }
    ],
    "check_point": {
        "lat": 59.947188,
        "lon": 30.313510,
        "geometry": {
            "type": "Feature",
            "properties": {"radius": 26.7},
            "geometry": {
                "type": "Point",
                "coordinates": [30.313358, 59.947241]
            }
        }
    }
}

def test_delete_station():
    create_resp = TransportAPI.create_station(STATION_DATA)
    assert create_resp.status_code in (200, 201)
    station_id = create_resp.json().get('data', {}).get('id')
    assert station_id
    delete_resp = TransportAPI.delete_station(station_id)
    assert delete_resp.status_code == 200
    json_data = delete_resp.json()
    assert json_data.get('success') is True
    assert 'data' in json_data 