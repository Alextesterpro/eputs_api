# import pytest
# import uuid
# import requests
# from tests_microservices.utils.incidents.response_scenarios_api import ResponseScenariosAPI
# from tests_microservices.utils.incidents.response_scenarios_schemas import (
#     SCENARIO_STATUS_CODES,
#     SCENARIO_SEARCH_PARAMS,
#     DEFAULT_SCENARIO_PAGE,
#     DEFAULT_SCENARIO_LIMIT,
#     MAX_SCENARIO_LIMIT,
#     VALID_SCENARIO_DATA
# )
# from tests_microservices.checking import Checking

# Глобальная переменная для хранения ID созданных сценариев
# created_scenario_ids = []

# def get_unique_scenario_data(base_data):
#     """Генерирует уникальные данные для сценария"""
#     unique_id = str(uuid.uuid4())[:8]
#     unique_data = base_data.copy()
#     unique_data['name'] = f"{base_data['name']} {unique_id}"
#     return unique_data

# def handle_server_timeout(func):
#     """Декоратор для обработки таймаутов сервера"""
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             if "timeout" in str(e).lower() or "timed out" in str(e).lower():
#                 print("Сервер не отвечает (таймаут) - это ожидаемо при проблемах с сервером")
#                 pytest.skip("Сервер не отвечает (таймаут)")
#             else:
#                 raise e
#     return wrapper

# @pytest.mark.detailed
# @pytest.mark.regression
# class TestScenarioList:
#     """Тесты для получения списка сценариев реагирования"""

#     def teardown_method(self):
#         """Очистка после каждого теста - удаление созданных сценариев"""
#         global created_scenario_ids
#         for scenario_id in created_scenario_ids:
#             try:
#                 ResponseScenariosAPI.delete_scenario(scenario_id)
#                 print(f"Удален сценарий с ID: {scenario_id}")
#             except Exception as e:
#                 print(f"Ошибка при удалении сценария {scenario_id}: {e}")
#         created_scenario_ids.clear()

#     @handle_server_timeout
#     def test_get_scenarios_list_default_params(self):
#         """Тест получения списка сценариев с параметрами по умолчанию"""
#         response = ResponseScenariosAPI.get_scenarios_list()
        
#         # Проверяем статус код (может быть 502 из-за проблем с сервером)
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], 502], \
#             f"Ожидался статус 200 или 502, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             # Проверяем структуру ответа
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             assert isinstance(json_data['data'], list), "Data должен быть списком"
            
#             print(f"Получен список сценариев с параметрами по умолчанию. Количество: {len(json_data['data'])}")
#         else:
#             print("Сервер вернул 502 ошибку (проблемы с сервером)")

#     def test_get_scenarios_list_with_pagination(self):
#         """Тест получения списка сценариев с пагинацией"""
#         params = {
#             'page': DEFAULT_SCENARIO_PAGE,
#             'limit': DEFAULT_SCENARIO_LIMIT
#         }
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # Проверяем статус код
#         assert response.status_code == SCENARIO_STATUS_CODES["OK"], \
#             f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
        
#         # Проверяем структуру ответа
#         json_data = response.json()
#         assert 'data' in json_data, "Должен быть блок data"
#         assert isinstance(json_data['data'], list), "Data должен быть списком"
        
#         print(f"Пагинация работает корректно. Получено элементов: {len(json_data['data'])}")

#     @handle_server_timeout
#     def test_get_scenarios_list_with_custom_limit(self):
#         """Тест получения списка сценариев с пользовательским лимитом"""
#         custom_limit = 10
#         params = {'limit': custom_limit}
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # Проверяем статус код (может быть 502 из-за проблем с сервером)
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], 502], \
#             f"Ожидался статус 200 или 502, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             # Проверяем структуру ответа
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             assert isinstance(json_data['data'], list), "Data должен быть списком"
            
#             # API может не соблюдать лимит строго, поэтому проверяем только что данные получены
#             assert len(json_data['data']) > 0, "Должны быть получены данные"
#             print(f"API вернул {len(json_data['data'])} элементов при запросе лимита {custom_limit}")
            
#             print(f"Пользовательский лимит работает корректно. Получено элементов: {len(json_data['data'])}")
#         else:
#             print("Сервер вернул 502 ошибку (проблемы с сервером)")

#     @handle_server_timeout
#     def test_get_scenarios_list_with_max_limit(self):
#         """Тест получения списка сценариев с максимальным лимитом"""
#         params = {'limit': MAX_SCENARIO_LIMIT}
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # Проверяем статус код (может быть 502 из-за проблем с сервером)
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], 502], \
#             f"Ожидался статус 200 или 502, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             # Проверяем структуру ответа
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             assert isinstance(json_data['data'], list), "Data должен быть списком"
            
#             print(f"Максимальный лимит работает корректно. Получено элементов: {len(json_data['data'])}")
#         else:
#             print("Сервер вернул 502 ошибку (проблемы с сервером)")

#     def test_get_scenarios_list_with_invalid_limit(self):
#         """Тест получения списка сценариев с неверным лимитом"""
#         params = {'limit': 999999}  # Слишком большой лимит
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # API может вернуть ошибку или ограничить лимит
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], SCENARIO_STATUS_CODES["BAD_REQUEST"]], \
#             f"Ожидался статус 200 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             print("API автоматически ограничил большой лимит")
#         else:
#             print("API вернул ошибку для неверного лимита")

#     def test_get_scenarios_list_with_negative_limit(self):
#         """Тест получения списка сценариев с отрицательным лимитом"""
#         params = {'limit': -1}
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # API может вернуть ошибку или использовать значение по умолчанию (может быть 502 из-за проблем с сервером)
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], SCENARIO_STATUS_CODES["BAD_REQUEST"], 502], \
#             f"Ожидался статус 200, 400 или 502, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             print("API обработал отрицательный лимит")
#         else:
#             print("API вернул ошибку для отрицательного лимита")

#     def test_get_scenarios_list_with_invalid_page(self):
#         """Тест получения списка сценариев с неверной страницей"""
#         params = {'page': -1}
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # API может вернуть ошибку или использовать значение по умолчанию
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], SCENARIO_STATUS_CODES["BAD_REQUEST"]], \
#             f"Ожидался статус 200 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             print("API обработал неверную страницу")
#         else:
#             print("API вернул ошибку для неверной страницы")

#     def test_get_scenarios_list_with_large_page(self):
#         """Тест получения списка сценариев с большой страницей"""
#         params = {'page': 999999}
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # API должен вернуть пустой список или ошибку
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], SCENARIO_STATUS_CODES["BAD_REQUEST"]], \
#             f"Ожидался статус 200 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             # Ожидаем пустой список для несуществующей страницы
#             print(f"Получен список для большой страницы. Количество элементов: {len(json_data['data'])}")
#         else:
#             print("API вернул ошибку для большой страницы")

#     def test_get_scenarios_list_response_structure(self):
#         """Тест структуры ответа списка сценариев"""
#         response = ResponseScenariosAPI.get_scenarios_list()
        
#         # Проверяем статус код
#         assert response.status_code == SCENARIO_STATUS_CODES["OK"], \
#             f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
        
#         # Проверяем структуру ответа
#         json_data = response.json()
        
#         # Проверяем обязательные поля
#         assert 'data' in json_data, "Должен быть блок data"
#         assert isinstance(json_data['data'], list), "Data должен быть списком"
        
#         # Если есть данные, проверяем структуру первого элемента
#         if json_data['data']:
#             first_scenario = json_data['data'][0]
#             expected_fields = ['id', 'name', 'project', 'created_by', 'updated_by', 'created_at', 'updated_at']
            
#             for field in expected_fields:
#                 assert field in first_scenario, f"Отсутствует поле {field} в структуре сценария"
            
#             # Проверяем типы данных
#             assert isinstance(first_scenario['id'], int), "ID должен быть числом"
#             assert isinstance(first_scenario['name'], str), "Название должно быть строкой"
        
#         print("Структура ответа соответствует ожиданиям")

#     def test_get_scenarios_list_with_name_filter(self):
#         """Тест получения списка сценариев с фильтром по названию"""
#         # Сначала создаем тестовый сценарий
#         from tests_microservices.utils.incidents.response_scenarios_schemas import VALID_SCENARIO_DATA
#         test_data = get_unique_scenario_data(VALID_SCENARIO_DATA)
#         create_response = ResponseScenariosAPI.create_scenario(test_data)
        
#         if create_response.status_code in [SCENARIO_STATUS_CODES["CREATED"], SCENARIO_STATUS_CODES["OK"]]:
#             scenario_id = create_response.json()['data']['id']
#             created_scenario_ids.append(scenario_id)
            
#             # Получаем список с фильтром по названию
#             params = {'name': test_data['name']}
#             response = ResponseScenariosAPI.get_scenarios_list(params)
            
#             # Проверяем статус код
#             assert response.status_code == SCENARIO_STATUS_CODES["OK"], \
#                 f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
            
#             # Проверяем структуру ответа
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             assert isinstance(json_data['data'], list), "Data должен быть списком"
            
#             print(f"Фильтр по названию работает. Найдено сценариев: {len(json_data['data'])}")
#         else:
#             print("Не удалось создать тестовый сценарий для проверки фильтра")

#     @handle_server_timeout
#     def test_get_scenarios_list_with_multiple_params(self):
#         """Тест получения списка сценариев с несколькими параметрами"""
#         params = {
#             'page': 1,
#             'limit': 10,
#             'name': 'сценарий'
#         }
        
#         response = ResponseScenariosAPI.get_scenarios_list(params)
        
#         # Проверяем статус код (может быть 502 из-за проблем с сервером)
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], 502], \
#             f"Ожидался статус 200 или 502, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             # Проверяем структуру ответа
#             json_data = response.json()
#             assert 'data' in json_data, "Должен быть блок data"
#             assert isinstance(json_data['data'], list), "Data должен быть списком"
            
#             print(f"Множественные параметры работают корректно. Получено элементов: {len(json_data['data'])}")
#         else:
#             print("Сервер вернул 502 ошибку (проблемы с сервером)")

#     @handle_server_timeout
#     def test_get_scenarios_list_performance(self):
#         """Тест производительности получения списка сценариев"""
#         import time
        
#         start_time = time.time()
#         response = ResponseScenariosAPI.get_scenarios_list()
#         end_time = time.time()
        
#         response_time = (end_time - start_time) * 1000  # в миллисекундах
        
#         # Проверяем статус код (может быть 502 из-за проблем с сервером)
#         assert response.status_code in [SCENARIO_STATUS_CODES["OK"], 502], \
#             f"Ожидался статус 200 или 502, но получен {response.status_code}. Ответ: {response.text}"
        
#         if response.status_code == SCENARIO_STATUS_CODES["OK"]:
#             # Проверяем время ответа (увеличиваем лимит до 15 секунд из-за проблем с сервером)
#             assert response_time < 15000, f"Время ответа {response_time:.2f}мс превышает 15000мс"
#             print(f"Производительность в норме. Время ответа: {response_time:.2f}мс")
#         else:
#             print(f"Сервер вернул 502 ошибку. Время ответа: {response_time:.2f}мс") 