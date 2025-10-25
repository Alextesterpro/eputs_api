from tests_microservices.utils.api import TransportAPI

def test_list_stations():
    response = TransportAPI.list_stations(page=1, limit=5)
    assert response.status_code == 200
    json_data = response.json()
    # Если ответ — список
    if isinstance(json_data, list):
        assert isinstance(json_data, list)
    # Если ответ — объект с ключом data
    elif isinstance(json_data, dict):
        if 'data' in json_data and isinstance(json_data['data'], list):
            assert isinstance(json_data['data'], list)
        elif 'data' in json_data and isinstance(json_data['data'], dict) and 'list' in json_data['data']:
            assert isinstance(json_data['data']['list'], list)
        else:
            raise AssertionError('Unexpected response structure: {}'.format(json_data))
    else:
        raise AssertionError('Unexpected response type: {}'.format(type(json_data))) 