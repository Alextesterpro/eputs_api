import pytest
from tests_microservices.utils.api import TransportAPI

BASE_DATA = {
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

@pytest.mark.parametrize("field,value,error_hint,expect_200", [
    ("name", "", "название", False),
    ("type_list", [], "тип", True),  # API возвращает 200, если type_list пустой
    ("check_point", {}, "check_point", False),
])
def test_create_station_invalid(field, value, error_hint, expect_200):
    data = BASE_DATA.copy()
    data[field] = value
    response = TransportAPI.create_station(data)
    if expect_200:
        assert response.status_code == 200
    else:
        assert response.status_code in (400, 422)
        json_data = response.json()
        assert 'error_description' in json_data
        if 'message' in json_data:
            if error_hint == 'check_point':
                found = any('check_point' in k for k in json_data['message'].keys())
                assert found, f"'check_point' not found in {json_data['message']}"
            else:
                found = any(error_hint.lower() in str(k).lower() or error_hint.lower() in str(v).lower() for k, v in json_data['message'].items())
                assert found, f"'{error_hint}' not found in {json_data['message']}"
        else:
            assert error_hint.lower() in json_data['error_description'].lower() 