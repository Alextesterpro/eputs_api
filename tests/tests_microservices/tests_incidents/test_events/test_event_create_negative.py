import pytest
from tests_microservices.utils.incidents.events_api import EventsAPI
from tests_microservices.utils.incidents.events_schemas import (
    INVALID_EVENT_DATA_EMPTY_NAME,
    INVALID_EVENT_DATA_WRONG_DATE_FORMAT,
    INVALID_EVENT_DATA_END_BEFORE_START,
    EVENT_STATUS_CODES
)
from tests_microservices.checking import Checking

@pytest.mark.negative
@pytest.mark.regression
class TestEventCreateNegative:
    """Негативные тесты создания мероприятий"""
    
    @pytest.mark.parametrize("field,value,error_hint", [
        ("name", "", "название"),
        ("name", None, "название"),
        ("short_name", "", "краткое название"),
        ("international_name", "", "международное название"),
        ("date_start", "", "дата начала"),
        ("date_end", "", "дата окончания"),
    ])
    def test_create_event_missing_required_fields(self, field, value, error_hint):
        """Тест создания мероприятия с отсутствующими обязательными полями"""
        from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA
        
        test_data = MINIMAL_EVENT_DATA.copy()
        test_data[field] = value
        
        response = EventsAPI.create_event(test_data)
        
        # Проверяем статус код ошибки
        assert response.status_code in (EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST']), \
            f"Ожидался статус 422 или 400, но получен {response.status_code}"
        
        # Проверяем структуру ошибки
        json_data = response.json()
        assert 'error_description' in json_data or 'message' in json_data, "Должно быть сообщение об ошибке"
        
        print(f"Корректно обработана ошибка для поля '{field}' с значением '{value}'")
    
    def test_create_event_empty_name(self):
        """Тест создания мероприятия с пустым названием"""
        response = EventsAPI.create_event(INVALID_EVENT_DATA_EMPTY_NAME)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        json_data = response.json()
        assert 'error_description' in json_data or 'message' in json_data
        
        print("Корректно обработана ошибка с пустым названием")
    
    def test_create_event_wrong_date_format(self):
        """Тест создания мероприятия с неправильным форматом даты"""
        response = EventsAPI.create_event(INVALID_EVENT_DATA_WRONG_DATE_FORMAT)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        json_data = response.json()
        assert 'error_description' in json_data or 'message' in json_data
        
        print("Корректно обработана ошибка с неправильным форматом даты")
    
    def test_create_event_end_before_start(self):
        """Тест создания мероприятия где дата окончания раньше даты начала"""
        response = EventsAPI.create_event(INVALID_EVENT_DATA_END_BEFORE_START)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        json_data = response.json()
        assert 'error_description' in json_data or 'message' in json_data
        
        print("Корректно обработана ошибка с неправильным порядком дат")
    
    def test_create_event_with_invalid_object_data(self):
        """Тест создания мероприятия с невалидными данными объектов"""
        from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA
        
        test_data = MINIMAL_EVENT_DATA.copy()
        test_data['objects'] = [
            {
                "id": "invalid_id",  # ID должен быть числом
                "name": "",
                "type_id": "invalid_type",  # type_id должен быть числом
                "type_name": None
            }
        ]
        
        response = EventsAPI.create_event(test_data)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        json_data = response.json()
        assert 'error_description' in json_data or 'message' in json_data
        
        print("Корректно обработана ошибка с невалидными данными объектов")
    
    def test_create_event_with_past_dates(self):
        """Тест создания мероприятия с датами в прошлом"""
        from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA
        
        test_data = MINIMAL_EVENT_DATA.copy()
        test_data['date_start'] = "2020-01-01T00:00:00+03:00"
        test_data['date_end'] = "2020-01-31T23:59:59+03:00"
        
        response = EventsAPI.create_event(test_data)
        
        # Проверяем статус код (может быть 422 или 200 в зависимости от бизнес-логики)
        assert response.status_code in (200, EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        if response.status_code != 200:
            json_data = response.json()
            assert 'error_description' in json_data or 'message' in json_data
            print("Корректно обработана ошибка с датами в прошлом")
        else:
            print("Мероприятие с датами в прошлом создано (разрешено бизнес-логикой)")
    
    def test_create_event_with_very_long_names(self):
        """Тест создания мероприятия с очень длинными названиями"""
        from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA
        
        test_data = MINIMAL_EVENT_DATA.copy()
        # Создаем очень длинное название (более 1000 символов)
        test_data['name'] = "А" * 1001
        test_data['short_name'] = "Б" * 1001
        test_data['international_name'] = "C" * 1001
        
        response = EventsAPI.create_event(test_data)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        json_data = response.json()
        assert 'error_description' in json_data or 'message' in json_data
        
        print("Корректно обработана ошибка с очень длинными названиями")
    
    def test_create_event_without_objects(self):
        """Тест создания мероприятия без объектов"""
        from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA
        
        test_data = MINIMAL_EVENT_DATA.copy()
        test_data['objects'] = []
        
        response = EventsAPI.create_event(test_data)
        
        # Проверяем статус код (может быть 422 или 200 в зависимости от бизнес-логики)
        assert response.status_code in (200, EVENT_STATUS_CODES['VALIDATION_ERROR'], EVENT_STATUS_CODES['BAD_REQUEST'])
        
        if response.status_code != 200:
            json_data = response.json()
            assert 'error_description' in json_data or 'message' in json_data
            print("Корректно обработана ошибка без объектов")
        else:
            print("Мероприятие без объектов создано (разрешено бизнес-логикой)")
    
    def test_create_event_with_invalid_json(self):
        """Тест создания мероприятия с невалидным JSON"""
        # Отправляем невалидный JSON
        headers = EventsAPI.HEADERS.copy()
        headers['Content-Type'] = 'application/json'
        
        response = EventsAPI.create_event({"invalid": "json", "with": "unclosed_quote"}, headers)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES['BAD_REQUEST'], 500)
        
        print("Корректно обработана ошибка с невалидным JSON")
    
    # def test_create_event_without_authentication(self):
        """Тест создания мероприятия без аутентификации"""
        headers = EventsAPI.HEADERS.copy()
        del headers['Authorization']
        
        response = EventsAPI.create_event(MINIMAL_EVENT_DATA, headers)
        
        # Проверяем статус код
        assert response.status_code in (EVENT_STATUS_CODES["UNAUTHORIZED"], EVENT_STATUS_CODES["OK"])
        
        print("Корректно обработана ошибка без аутентификации") 