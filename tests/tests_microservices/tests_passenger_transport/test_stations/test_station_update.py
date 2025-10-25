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

def test_update_station():
    create_resp = TransportAPI.create_station(STATION_DATA)
    assert create_resp.status_code in (200, 201)
    station_id = create_resp.json().get('data', {}).get('id')
    assert station_id
    update_data = STATION_DATA.copy()
    update_data["name"] = "Остановка обновлённая"
    update_resp = TransportAPI.update_station(station_id, update_data)
    assert update_resp.status_code == 200
    json_data = update_resp.json()
    assert json_data.get('success') is True
    assert 'data' in json_data
    assert isinstance(json_data['data'], dict)
    assert json_data['data']['id'] == station_id
    assert json_data['data']['name'] == "Остановка обновлённая" 