# import pytest
# from tests_microservices.utils.incidents.events_api import EventsAPI

# @pytest.mark.regression
# class TestEventList:
#     """Тесты получения списка мероприятий - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

#     # def test_get_events_list_success(self):
#     #     """Тест успешного получения списка мероприятий - ДУБЛИКАТ с basic"""
#     #     response = EventsAPI.list_events()
#     #     assert response.status_code == 200
#     #     
#     #     data = response.json()
#     #     assert 'data' in data
#     #     print(f"Получено мероприятий: {len(data['data'])}")

#     # def test_get_events_list_with_pagination(self):
#     #     """Тест получения списка мероприятий с пагинацией - ИЗБЫТОЧНЫЙ"""
#     #     params = {'page': 1, 'limit': 10}
#     #     response = EventsAPI.list_events(params)
#     #     assert response.status_code == 200
#     #     print("Список мероприятий с пагинацией получен")

#     # def test_get_events_list_with_search(self):
#     #     """Тест получения списка мероприятий с поиском - ИЗБЫТОЧНЫЙ"""
#     #     params = {'search': 'тест'}
#     #     response = EventsAPI.list_events(params)
#     #     assert response.status_code == 200
#     #     print("Список мероприятий с поиском получен")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_event_basic.py 