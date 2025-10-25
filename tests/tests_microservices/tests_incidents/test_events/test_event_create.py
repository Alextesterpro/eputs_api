# import pytest
# import time
# from tests_microservices.utils.incidents.events_api import EventsAPI
# from tests_microservices.utils.incidents.events_schemas import (
#     VALID_EVENT_DATA, 
#     MINIMAL_EVENT_DATA,
#     EVENT_RESPONSE_SCHEMA,
#     EVENT_DATA_SCHEMA,
#     EVENT_STATUS_CODES,
#     MAX_EVENT_RESPONSE_TIME
# )
# from tests_microservices.checking import Checking

# # Глобальная переменная для хранения ID созданных событий
# created_event_ids = []

# @pytest.mark.detailed
# @pytest.mark.regression
# class TestEventCreate:
#     """Тесты создания мероприятий - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

#     def teardown_method(self):
#         """Очистка после каждого теста - удаление созданных событий"""
#         global created_event_ids
#         for event_id in created_event_ids:
#             try:
#                 EventsAPI.delete_event(event_id)
#                 print(f"Удалено событие с ID: {event_id}")
#             except Exception as e:
#                 print(f"Ошибка при удалении события {event_id}: {e}")
#         created_event_ids.clear()
    
#     # def test_create_event_with_full_data(self):
#     #     """Тест создания мероприятия с полными данными - ДУБЛИКАТ с basic"""
#     #     start_time = time.time()
#     #     response = EventsAPI.create_event(VALID_EVENT_DATA)
#     #     response_time = (time.time() - start_time) * 1000
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем время ответа
#     #     Checking.check_response_time(response, MAX_EVENT_RESPONSE_TIME)
#     #     
#     #     # Проверяем структуру ответа
#     #     json_data = response.json()
#     #     Checking.check_json_token(response, ['success', 'data'])
#     #     
#     #     # Проверяем успешность операции
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     
#     #     # Проверяем данные мероприятия
#     #     event_data = json_data['data']
#     #     assert event_data['name'] == VALID_EVENT_DATA['name'], "Название должно совпадать"
#     #     assert 'id' in event_data, "Должен быть ID мероприятия"
#     #     assert isinstance(event_data['id'], int), "ID должен быть числом"
#     #     
#     #     # Сохраняем ID для последующего удаления
#     #     created_event_ids.append(event_data['id'])
#     #     
#     #     # Проверяем схему данных
#     #     Checking.check_json_schema(response, EVENT_DATA_SCHEMA)
#     #     
#     #     print(f"Мероприятие создано успешно. ID: {event_data['id']}, Время ответа: {response_time:.2f}ms")
    
#     # def test_create_event_with_minimal_data(self):
#     #     """Тест создания мероприятия с минимальными данными - ДУБЛИКАТ с basic"""
#     #     response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем структуру ответа
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     
#     #     # Проверяем данные мероприятия
#     #     event_data = json_data['data']
#     #     assert event_data['name'] == MINIMAL_EVENT_DATA['name'], "Название должно совпадать"
#     #     
#     #     # Сохраняем ID для последующего удаления
#     #     created_event_ids.append(event_data['id'])
#     #     
#     #     print(f"Мероприятие с минимальными данными создано. ID: {event_data['id']}")
    
#     # def test_create_event_with_special_characters(self):
#     #     """Тест создания мероприятия со специальными символами в названии - ИЗБЫТОЧНЫЙ"""
#     #     test_data = MINIMAL_EVENT_DATA.copy()
#     #     test_data['name'] = "Мероприятие с символами: !@#$%^&*()_+-=[]{}|;':\",./<>?"
#     #     
#     #     response = EventsAPI.create_event(test_data)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
#     #     
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     assert json_data['data']['name'] == test_data['name'], "Название со спецсимволами должно сохраниться"
#     #     
#     #     # Сохраняем ID для последующего удаления
#     #     created_event_ids.append(json_data['data']['id'])
#     #     
#     #     print(f"Мероприятие со спецсимволами создано. ID: {json_data['data']['id']}")
    
#     # def test_create_event_with_long_names(self):
#     #     """Тест создания мероприятия с длинными названиями - ИЗБЫТОЧНЫЙ"""
#     #     long_names = [
#     #         "Очень длинное название мероприятия с множеством символов для проверки ограничений системы",
#     #         "A" * 100,  # 100 символов A
#     #         "Тест" * 25  # 100 символов "Тест"
#     #     ]
#     #     
#     #     for name in long_names:
#     #         test_data = MINIMAL_EVENT_DATA.copy()
#     #         test_data['name'] = name
#     #         
#     #         response = EventsAPI.create_event(test_data)
#     #         
#     #         # Проверяем статус код
#     #         assert response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"], EVENT_STATUS_CODES["BAD_REQUEST"]), f"Неожиданный статус код: {response.status_code}"
#     #         
#     #         if response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]):
#     #             json_data = response.json()
#     #             assert json_data['success'] is True, "Операция должна быть успешной"
#     #             created_event_ids.append(json_data['data']['id'])
#     #             print(f"Длинное название '{name[:30]}...' создано. ID: {json_data['data']['id']}")
#     #         else:
#     #             print(f"Длинное название '{name[:30]}...' отклонено сервером")
    
#     # def test_create_event_with_numbers(self):
#     #     """Тест создания мероприятия с числами в названии - ИЗБЫТОЧНЫЙ"""
#     #     test_data = MINIMAL_EVENT_DATA.copy()
#     #     test_data['name'] = "Мероприятие 2025 №123"
#     #     
#     #     response = EventsAPI.create_event(test_data)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
#     #     
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     assert json_data['data']['name'] == test_data['name'], "Название с числами должно сохраниться"
#     #     
#     #     # Сохраняем ID для последующего удаления
#     #     created_event_ids.append(json_data['data']['id'])
#     #     
#     #     print(f"Мероприятие с числами создано. ID: {json_data['data']['id']}")
    
#     # def test_create_event_with_unicode(self):
#     #     """Тест создания мероприятия с Unicode символами - ИЗБЫТОЧНЫЙ"""
#     #     test_data = MINIMAL_EVENT_DATA.copy()
#     #     test_data['name'] = "Мероприятие с эмодзи 🎉🎊🎈 и кириллицей"
#     #     
#     #     response = EventsAPI.create_event(test_data)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
#     #     
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     assert json_data['data']['name'] == test_data['name'], "Название с Unicode должно сохраниться"
#     #     
#     #     # Сохраняем ID для последующего удаления
#     #     created_event_ids.append(json_data['data']['id'])
#     #     
#     #     print(f"Мероприятие с Unicode создано. ID: {json_data['data']['id']}")
    
#     # def test_create_multiple_events(self):
#     #     """Тест создания множественных мероприятий - ИЗБЫТОЧНЫЙ"""
#     #     events_to_create = 5
#     #     created_count = 0
#     #     
#     #     for i in range(events_to_create):
#     #         test_data = MINIMAL_EVENT_DATA.copy()
#     #         test_data['name'] = f"Множественное мероприятие {i+1}"
#     #         
#     #         response = EventsAPI.create_event(test_data)
#     #         
#     #         if response.status_code in (EVENT_STATUS_CODES["CREATED"], EVENT_STATUS_CODES["OK"]):
#     #             json_data = response.json()
#     #             if json_data['success'] is True:
#     #                 created_event_ids.append(json_data['data']['id'])
#     #                 created_count += 1
#     #                 print(f"Создано мероприятие {i+1}. ID: {json_data['data']['id']}")
#     #         
#     #     assert created_count == events_to_create, f"Создано {created_count} из {events_to_create} мероприятий"
#     #     print(f"Успешно создано {created_count} мероприятий")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_event_basic.py 