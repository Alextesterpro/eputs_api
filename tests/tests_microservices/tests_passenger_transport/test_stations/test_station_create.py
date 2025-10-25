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

def test_create_station():
    response = TransportAPI.create_station(STATION_DATA)
    assert response.status_code in (200, 201)
    json_data = response.json()
    assert json_data.get('success') is True
    assert 'data' in json_data
    assert isinstance(json_data['data'], dict)
    assert 'id' in json_data['data']
    assert isinstance(json_data['data']['id'], int)
    assert json_data['data']['name'] == STATION_DATA['name'] 