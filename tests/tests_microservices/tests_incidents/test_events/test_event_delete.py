# import pytest
# from tests_microservices.utils.incidents.events_api import EventsAPI
# from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA

# # Глобальная переменная для хранения ID созданных событий
# created_event_ids = []

# @pytest.mark.regression
# class TestEventDelete:
#     """Тесты удаления мероприятий - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

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

#     # def test_delete_event_success(self):
#     #     """Тест успешного удаления мероприятия - ДУБЛИКАТ с basic"""
#     #     # Создаем мероприятие для удаления
#     #     create_response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
#     #     assert create_response.status_code in (200, 201)
#     #     event_id = create_response.json()['data']['id']
#     #     created_event_ids.append(event_id)
#     #     
#     #     # Удаляем мероприятие
#     #     response = EventsAPI.delete_event(event_id)
#     #     assert response.status_code == 200
#     #     
#     #     data = response.json()
#     #     assert data['success'] is True
#     #     
#     #     print(f"Мероприятие {event_id} успешно удалено")

#     # def test_delete_event_not_found(self):
#     #     """Тест удаления несуществующего мероприятия - ИЗБЫТОЧНЫЙ"""
#     #     response = EventsAPI.delete_event(99999)
#     #     assert response.status_code in (404, 400)
#     #     print("Корректно обработана ошибка удаления несуществующего мероприятия")

#     # def test_delete_event_invalid_id(self):
#     #     """Тест удаления мероприятия с неверным ID - ИЗБЫТОЧНЫЙ"""
#     #     response = EventsAPI.delete_event("invalid_id")
#     #     assert response.status_code in (404, 400)
#     #     print("Корректно обработана ошибка удаления с неверным ID")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_event_basic.py 