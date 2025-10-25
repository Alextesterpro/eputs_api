import pytest
from tests_microservices.utils.incidents.events_api import EventsAPI
from tests_microservices.utils.incidents.events_schemas import EVENT_STATUS_CODES
from tests_microservices.checking import Checking

@pytest.mark.real_data
@pytest.mark.regression
class TestEventRealData:
    """Тесты с реальными данными из cURL запросов"""
    
    def test_update_event_with_real_data(self):
        """Тест обновления мероприятия с реальными данными из cURL"""
        # Реальные данные из cURL запроса
        real_update_data = {
            "name": "тест555",
            "short_name": "тест4434", 
            "international_name": "тест4545",
            "date_start": "2020-02-02T03:00:00+03:00",
            "date_end": "2020-12-30T03:00:00+03:00",
            "objects": [
                {
                    "id": 27,
                    "project": "98_spb",
                    "name": "ДИТ_155",
                    "description": "А-121 \"Сортавала\" Санкт-Петербург - Сортавала - автомобильная дорога Р-21 \"Кола\". \nУчасток: 4 очередь: км 36+000 – км 57+550",
                    "type_id": 69,
                    "type": {
                        "id": 69,
                        "project": "98_spb",
                        "name": "ДИТ",
                        "created_by": None,
                        "updated_by": None,
                        "created_at": "2025-03-31T15:03:57.000000Z",
                        "updated_at": "2025-03-31T15:03:57.000000Z"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [30.195523, 60.497795]
                    },
                    "organization_id": 0,
                    "is_subscribe": False,
                    "organization": {
                        "id": 0,
                        "title": "Организация по умолчанию",
                        "project": "98_spb",
                        "phones": [],
                        "emails": [],
                        "inn": "0000000000000",
                        "juristic_address_id": None,
                        "mail_address_id": None,
                        "real_address_id": None,
                        "created_by": None,
                        "updated_by": None,
                        "deleted_by": None,
                        "deleted_at": None,
                        "created_at": "2024-08-28T09:32:38.000000Z",
                        "updated_at": "2024-08-28T09:32:38.000000Z",
                        "full_name": "Организация по умолчанию",
                        "attachments": [],
                        "source": 1,
                        "juristic_address": None,
                        "mail_address": None,
                        "real_address": None,
                        "persons": []
                    },
                    "lat": "60.497795",
                    "lon": "30.195523",
                    "address": [],
                    "events": [
                        {
                            "id": 38,
                            "event_id": 48,
                            "infrastructure_id": 27,
                            "event_name": "Добавление",
                            "event": {
                                "id": 48,
                                "name": "Добавление",
                                "project": "98_spb",
                                "date_end": "2025-07-31T07:55:00+00:00",
                                "created_at": "2025-07-23T06:45:16.000000Z",
                                "created_by": None,
                                "date_start": "2025-07-01T06:45:10+00:00",
                                "deleted_at": None,
                                "deleted_by": None,
                                "short_name": "краткое",
                                "updated_at": "2025-07-23T06:45:16.000000Z",
                                "updated_by": None,
                                "international_name": "международное"
                            },
                            "created_at": "2025-07-23T06:45:16.000000Z",
                            "updated_at": "2025-07-23T06:45:16.000000Z",
                            "deleted_at": None
                        }
                    ],
                    "repair_objects": [],
                    "address_text": "км 50+038 (прямой-обратный ход)",
                    "cadastre": None,
                    "created_by": None,
                    "updated_by": None,
                    "deleted_by": None,
                    "created_at": "2025-03-31T15:03:57.000000Z",
                    "updated_at": "2025-03-31T15:03:57.000000Z",
                    "deleted_at": None,
                    "type_name": "ДИТ"
                }
            ]
        }
        
        # Используем реальный ID из cURL запроса
        event_id = 20
        
        # Проверяем, что мероприятие существует
        get_response = EventsAPI.get_event(event_id)
        
        if get_response.status_code == EVENT_STATUS_CODES['OK']:
            # Обновляем мероприятие
            response = EventsAPI.update_event(event_id, real_update_data)
            
            # Проверяем статус код
            Checking.check_status_code(response, EVENT_STATUS_CODES['OK'])
            
            # Проверяем структуру ответа
            json_data = response.json()
            Checking.check_json_token(response, ['success', 'data'])
            
            # Проверяем успешность операции
            assert json_data['success'] is True, "Операция должна быть успешной"
            
            # Проверяем обновленные данные
            event_data = json_data['data']
            assert event_data['id'] == event_id, "ID должен совпадать"
            assert event_data['name'] == real_update_data['name'], "Название должно обновиться"
            assert event_data['short_name'] == real_update_data['short_name'], "Краткое название должно обновиться"
            assert event_data['international_name'] == real_update_data['international_name'], "Международное название должно обновиться"
            
            print(f"Мероприятие {event_id} обновлено с реальными данными")
        else:
            print(f"Мероприятие {event_id} не найдено, пропускаем тест")
            pytest.skip(f"Мероприятие {event_id} не существует")
    
    def test_delete_event_with_real_id(self):
        """Тест удаления мероприятия с реальным ID из cURL"""
        # Используем реальный ID из cURL запроса
        event_id = 23
        
        # Проверяем, что мероприятие существует
        get_response = EventsAPI.get_event(event_id)
        
        if get_response.status_code == EVENT_STATUS_CODES['OK']:
            # Удаляем мероприятие
            response = EventsAPI.delete_event(event_id)
            
            # Проверяем статус код
            Checking.check_status_code(response, EVENT_STATUS_CODES['OK'])
            
            # Проверяем структуру ответа
            json_data = response.json()
            Checking.check_json_token(response, ['success'])
            
            # Проверяем успешность операции
            assert json_data['success'] is True, "Операция должна быть успешной"
            
            # Проверяем, что мероприятие действительно удалено
            get_response_after_delete = EventsAPI.get_event(event_id)
            assert get_response_after_delete.status_code == EVENT_STATUS_CODES['NOT_FOUND'], \
                "Мероприятие должно быть удалено"
            
            print(f"Мероприятие {event_id} удалено")
        else:
            print(f"Мероприятие {event_id} не найдено, пропускаем тест")
            pytest.skip(f"Мероприятие {event_id} не существует")
    
    def test_get_existing_events(self):
        """Тест получения существующих мероприятий"""
        # Тестируем получение мероприятий с реальными ID
        real_event_ids = [20, 23, 48, 49, 43, 32]
        
        for event_id in real_event_ids:
            response = EventsAPI.get_event(event_id)
            
            if response.status_code == EVENT_STATUS_CODES['OK']:
                json_data = response.json()
                assert json_data['success'] is True
                assert json_data['data']['id'] == event_id
                print(f"Мероприятие {event_id} найдено: {json_data['data']['name']}")
            elif response.status_code == EVENT_STATUS_CODES['NOT_FOUND']:
                print(f"Мероприятие {event_id} не найдено (ожидаемо)")
            else:
                print(f"Неожиданный статус {response.status_code} для мероприятия {event_id}")
    
    def test_update_event_partial_real_data(self):
        """Тест частичного обновления с реальными данными"""
        event_id = 20
        
        # Проверяем, что мероприятие существует
        get_response = EventsAPI.get_event(event_id)
        
        if get_response.status_code == EVENT_STATUS_CODES['OK']:
            # Обновляем только название
            partial_update_data = {
                "name": "Обновленное название из теста",
                "short_name": "Обновленный"
            }
            
            response = EventsAPI.update_event(event_id, partial_update_data)
            
            # Проверяем статус код
            Checking.check_status_code(response, EVENT_STATUS_CODES['OK'])
            
            json_data = response.json()
            assert json_data['success'] is True
            
            # Проверяем обновленные данные
            event_data = json_data['data']
            assert event_data['name'] == partial_update_data['name'], "Название должно обновиться"
            assert event_data['short_name'] == partial_update_data['short_name'], "Краткое название должно обновиться"
            
            print(f"Частичное обновление мероприятия {event_id} выполнено")
        else:
            print(f"Мероприятие {event_id} не найдено, пропускаем тест")
            pytest.skip(f"Мероприятие {event_id} не существует") 