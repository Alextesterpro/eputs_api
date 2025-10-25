import pytest
import allure
from tests.tests_microservices.checking import Checking
from tests.tests_microservices.utils.api import TransportAPI
from tests.tests_microservices.utils.schemas import (
    ROUTE_CREATE_SCHEMA,
    STATUS_CODES,
    ROUTE_CATEGORIES,
    TEST_ROUTE_DATA,
    MAX_RESPONSE_TIME
)

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

@allure.epic('TestRouteCreate')
class TestRouteCreate:
    """Тесты для создания маршрутов"""

    @allure.description('Проверка создания маршрута')
    def test_create_route(self):
        """Тест создания маршрута"""
        data = ROUTE_DATA.copy()
        response = TransportAPI.create_route(**data)
        assert response.status_code in (200, 201)
        route_id = response.json().get('data', {}).get('id')
        assert route_id

    @allure.description('Проверка создания маршрутов разных категорий')
    @pytest.mark.parametrize("category_id,group_num", [
        (ROUTE_CATEGORIES['BUS'], '123 А'),
        (ROUTE_CATEGORIES['TRAM'], '456 Б'),
        (ROUTE_CATEGORIES['TROLLEYBUS'], '789 В')
    ])
    def test_create_routes_different_categories(self, category_id, group_num):
        """Тест проверки создания маршрутов разных категорий"""
        data = ROUTE_DATA.copy()
        data['category_id'] = category_id
        data['group_num'] = group_num
        data['num'] = group_num
        response = TransportAPI.create_route(**data)
        assert response.status_code in (200, 201)
        route_id = response.json().get('data', {}).get('id')
        assert route_id

    @allure.description('Проверка создания маршрута с невалидными данными')
    @pytest.mark.parametrize("category_id,group_num,group_order,expected_status", [
        (999, '123 А', 1, STATUS_CODES['VALIDATION_ERROR']),
        (ROUTE_CATEGORIES['BUS'], '', 1, STATUS_CODES['VALIDATION_ERROR']),
        (ROUTE_CATEGORIES['BUS'], '123 А', -1, STATUS_CODES['VALIDATION_ERROR']),
        (ROUTE_CATEGORIES['BUS'], '123 А', 1, STATUS_CODES['CREATED'])
    ])
    def test_create_route_invalid_data(self, category_id, group_num, group_order, expected_status):
        """Тест проверки создания маршрута с невалидными данными"""
        data = ROUTE_DATA.copy()
        data['category_id'] = category_id
        data['group_num'] = group_num
        data['group_order'] = group_order
        data['num'] = group_num
        response = TransportAPI.create_route(**data)
        if expected_status == STATUS_CODES['CREATED']:
            assert response.status_code in (200, 201)
            route_id = response.json().get('data', {}).get('id')
            assert route_id
        else:
            assert response.status_code == expected_status

    def test_delete_route(self):
        data = ROUTE_DATA.copy()
        create_resp = TransportAPI.create_route(**data)
        assert create_resp.status_code in (200, 201)
        route_id = create_resp.json().get('data', {}).get('id')
        assert route_id
        delete_resp = TransportAPI.delete_route(route_id=route_id, headers={"project": "98_spb"})
        assert delete_resp.status_code == 200

    def test_update_route(self):
        create_resp = TransportAPI.create_route(**ROUTE_DATA)
        assert create_resp.status_code in (200, 201)
        route_id = create_resp.json().get('data', {}).get('id')
        assert route_id
        update_data = ROUTE_DATA.copy()
        update_data['name'] = "Новое имя"
        update_data['duration'] = 42
        update_resp = TransportAPI.update_route(route_id, update_data)
        assert update_resp.status_code == 200

    @pytest.mark.parametrize("field,value,expected_status", [
        ("name", "", 422),  # пустое имя
        ("type_list", [], 200),  # пустой список типов
        ("check_point", {}, 422),  # пустой check_point
    ])
    def test_create_station_invalid(self, field, value, expected_status):
        data = {
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
        data[field] = value
        response = TransportAPI.create_station(data)
        assert response.status_code == expected_status

    def test_update_nonexistent_station(self):
        update_data = {
            "name": "Несуществующая остановка"
        }
        response = TransportAPI.update_station(999999, update_data)
        assert response.status_code in (404, 422)

    def test_delete_nonexistent_station(self):
        response = TransportAPI.delete_station(999999)
        assert response.status_code in (404, 422)

    def test_get_nonexistent_station(self):
        response = TransportAPI.get_station(999999)
        assert response.status_code in (404, 422) 