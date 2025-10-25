# import pytest
# from tests_microservices.utils.incidents.events_api import EventsAPI
# from tests_microservices.utils.incidents.events_schemas import MINIMAL_EVENT_DATA

# # Глобальная переменная для хранения ID созданных событий
# created_event_ids = []

# @pytest.mark.regression
# class TestEventUpdate:
#     """Тесты обновления мероприятий - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

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

#     # def test_update_event_success(self):
#     #     """Тест успешного обновления мероприятия - ДУБЛИКАТ с basic"""
#     #     # Создаем мероприятие
#     #     create_response = EventsAPI.create_event(MINIMAL_EVENT_DATA)
#     #     assert create_response.status_code in (200, 201)
#     #     event_id = create_response.json()['data']['id']
#     #     created_event_ids.append(event_id)
#     #     
#     #     # Обновляем мероприятие
#     #     update_data = {"name": "Обновленное мероприятие"}
#     #     response = EventsAPI.update_event(event_id, update_data)
#     #     assert response.status_code == 200
#     #     
#     #     data = response.json()
#     #     assert data['data']['name'] == "Обновленное мероприятие"
#     #     
#     #     print(f"Мероприятие {event_id} успешно обновлено")

#     # def test_update_event_not_found(self):
#     #     """Тест обновления несуществующего мероприятия - ИЗБЫТОЧНЫЙ"""
#     #     update_data = {"name": "Обновленное мероприятие"}
#     #     response = EventsAPI.update_event(99999, update_data)
#     #     assert response.status_code == 404
#     #     print("Корректно обработана ошибка обновления несуществующего мероприятия")

#     # def test_update_event_invalid_id(self):
#     #     """Тест обновления мероприятия с неверным ID - ИЗБЫТОЧНЫЙ"""
#     #     update_data = {"name": "Обновленное мероприятие"}
#     #     response = EventsAPI.update_event("invalid_id", update_data)
#     #     assert response.status_code in (404, 400)
#     #     print("Корректно обработана ошибка обновления с неверным ID")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_event_basic.py 