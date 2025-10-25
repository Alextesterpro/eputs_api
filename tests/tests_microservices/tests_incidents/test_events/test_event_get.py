# import pytest
# from tests_microservices.utils.incidents.events_api import EventsAPI
# from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA

# # Глобальная переменная для хранения ID созданных событий
# created_event_ids = []

# @pytest.mark.regression
# class TestEventGet:
#     """Тесты получения мероприятий - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

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

#     # def test_get_event_success(self):
#     #     """Тест успешного получения мероприятия - ДУБЛИКАТ с basic"""
#     #     # Создаем мероприятие
#     #     create_response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
#     #     assert create_response.status_code in (200, 201)
#     #     event_id = create_response.json()['data']['id']
#     #     created_event_ids.append(event_id)
#     #     
#     #     # Получаем мероприятие
#     #     response = EventsAPI.get_event(event_id)
#     #     assert response.status_code == 200
#     #     
#     #     data = response.json()
#     #     assert data['data']['id'] == event_id
#     #     
#     #     print(f"Мероприятие {event_id} успешно получено")

#     # def test_get_event_not_found(self):
#     #     """Тест получения несуществующего мероприятия - ИЗБЫТОЧНЫЙ"""
#     #     response = EventsAPI.get_event(99999)
#     #     assert response.status_code == 404
#     #     print("Корректно обработана ошибка получения несуществующего мероприятия")

#     # def test_get_event_invalid_id(self):
#     #     """Тест получения мероприятия с неверным ID - ИЗБЫТОЧНЫЙ"""
#     #     response = EventsAPI.get_event("invalid_id")
#     #     assert response.status_code in (404, 400)
#     #     print("Корректно обработана ошибка получения с неверным ID")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_event_basic.py 