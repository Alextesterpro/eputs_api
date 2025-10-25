# import pytest
# import time
# from tests_microservices.utils.incidents.categories_api import CategoriesAPI
# from tests_microservices.utils.incidents.categories_schemas import (
#     CATEGORY_LIST_SCHEMA,
#     CATEGORY_STATUS_CODES,
#     MAX_CATEGORY_RESPONSE_TIME,
#     DEFAULT_CATEGORY_PAGE,
#     DEFAULT_CATEGORY_LIMIT,
#     MAX_CATEGORY_LIMIT,
#     CATEGORY_SEARCH_PARAMS
# )
# from tests_microservices.checking import Checking

# # Глобальная переменная для хранения ID созданных категорий
# created_category_ids = []

# @pytest.mark.detailed
# @pytest.mark.regression
# class TestCategoryList:
#     """Тесты получения списка категорий (рисков) - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

#     def teardown_method(self):
#         """Очистка после каждого теста - удаление созданных категорий"""
#         global created_category_ids
#         for category_id in created_category_ids:
#             try:
#                 CategoriesAPI.delete_category(category_id)
#                 print(f"Удалена категория с ID: {category_id}")
#             except Exception as e:
#                 print(f"Ошибка при удалении категории {category_id}: {e}")
#         created_category_ids.clear()
    
#     # def test_get_categories_list_default_params(self):
#     #     """Тест получения списка категорий с параметрами по умолчанию - ДУБЛИКАТ с basic"""
#     #     response = CategoriesAPI.get_categories_list()
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем структуру ответа
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     assert 'data' in json_data, "Должен быть список данных"
#     #     assert isinstance(json_data['data'], list), "Данные должны быть списком"
#     #     
#     #     # Проверяем схему данных
#     #     Checking.check_json_schema(response, CATEGORY_LIST_SCHEMA)
#     #     
#     #     print(f"Получен список категорий с параметрами по умолчанию. Количество: {len(json_data['data'])}")
    
#     # def test_get_categories_list_with_pagination(self):
#     #     """Тест получения списка категорий с пагинацией - ИЗБЫТОЧНЫЙ"""
#     #     params = {
#     #         'page': 1,
#     #         'limit': 10
#     #     }
#     #     
#     #     response = CategoriesAPI.get_categories_list(params)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем структуру ответа
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     assert 'data' in json_data, "Должен быть список данных"
#     #     assert 'meta' in json_data, "Должна быть метаинформация"
#     #     
#     #     # Проверяем пагинацию
#     #     meta = json_data['meta']
#     #     assert 'current_page' in meta, "Должна быть текущая страница"
#     #     assert 'per_page' in meta, "Должно быть количество элементов на странице"
#     #     assert meta['current_page'] == params['page'], "Номер страницы должен совпадать"
#     #     assert meta['per_page'] == params['limit'], "Лимит должен совпадать"
#     #     
#     #     print(f"Получен список категорий с пагинацией. Страница: {meta['current_page']}, Элементов: {len(json_data['data'])}")
    
#     # def test_get_categories_list_with_different_limits(self):
#     #     """Тест получения списка категорий с разными лимитами - ИЗБЫТОЧНЫЙ"""
#     #     limits = [5, 10, 25, 50]
#     #     
#     #     for limit in limits:
#     #         params = {'limit': limit}
#     #         response = CategoriesAPI.get_categories_list(params)
#     #         
#     #         # Проверяем статус код
#     #         assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #         
#     #         # Проверяем данные
#     #         json_data = response.json()
#     #         assert json_data['success'] is True, "Операция должна быть успешной"
#     #         
#     #         # Проверяем, что количество элементов не превышает лимит
#     #         assert len(json_data['data']) <= limit, f"Количество элементов {len(json_data['data'])} превышает лимит {limit}"
#     #         
#     #         print(f"Лимит {limit}: получено {len(json_data['data'])} элементов")
    
#     # def test_get_categories_list_max_limit(self):
#     #     """Тест получения списка категорий с максимальным лимитом - ИЗБЫТОЧНЫЙ"""
#     #     params = {'limit': MAX_CATEGORY_LIMIT}
#     #     response = CategoriesAPI.get_categories_list(params)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем данные
#     #     json_data = response.json()
#     #     assert json_data['success'] is True, "Операция должна быть успешной"
#     #     assert len(json_data['data']) <= MAX_CATEGORY_LIMIT, f"Количество элементов превышает максимальный лимит"
#     #     
#     #     print(f"Максимальный лимит {MAX_CATEGORY_LIMIT}: получено {len(json_data['data'])} элементов")
    
#     # def test_get_categories_list_invalid_page(self):
#     #     """Тест получения списка категорий с неверной страницей - ИЗБЫТОЧНЫЙ"""
#     #     params = {'page': -1}
#     #     response = CategoriesAPI.get_categories_list(params)
#     #     
#     #     # Проверяем статус код (может быть 400 или 200 с пустым списком)
#     #     assert response.status_code in [200, 400], f"Неожиданный статус код: {response.status_code}"
#     #     
#     #     print(f"Тест с неверной страницей завершен. Статус: {response.status_code}")
    
#     # def test_get_categories_list_invalid_limit(self):
#     #     """Тест получения списка категорий с неверным лимитом - ИЗБЫТОЧНЫЙ"""
#     #     params = {'limit': -1}
#     #     response = CategoriesAPI.get_categories_list(params)
#     #     
#     #     # Проверяем статус код (может быть 400 или 200 с пустым списком)
#     #     assert response.status_code in [200, 400], f"Неожиданный статус код: {response.status_code}"
#     #     
#     #     print(f"Тест с неверным лимитом завершен. Статус: {response.status_code}")
    
#     # def test_get_categories_list_zero_limit(self):
#     #     """Тест получения списка категорий с нулевым лимитом - ИЗБЫТОЧНЫЙ"""
#     #     params = {'limit': 0}
#     #     response = CategoriesAPI.get_categories_list(params)
#     #     
#     #     # Проверяем статус код (может быть 400 или 200 с пустым списком)
#     #     assert response.status_code in [200, 400], f"Неожиданный статус код: {response.status_code}"
#     #     
#     #     print(f"Тест с нулевым лимитом завершен. Статус: {response.status_code}")
    
#     # def test_get_categories_list_very_large_limit(self):
#     #     """Тест получения списка категорий с очень большим лимитом - ИЗБЫТОЧНЫЙ"""
#     #     params = {'limit': 999999}
#     #     response = CategoriesAPI.get_categories_list(params)
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code in [200, 400], f"Неожиданный статус код: {response.status_code}"
#     #     
#     #     print(f"Тест с очень большим лимитом завершен. Статус: {response.status_code}")
    
#     # def test_get_categories_list_structure(self):
#     #     """Тест структуры ответа списка категорий - ИЗБЫТОЧНЫЙ"""
#     #     response = CategoriesAPI.get_categories_list()
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем схему данных
#     #     Checking.check_json_schema(response, CATEGORY_LIST_SCHEMA)
#     #     
#     #     print("Структура ответа списка категорий корректна")
    
#     # def test_get_categories_list_without_authentication(self):
#     #     """Тест получения списка категорий без авторизации - ИЗБЫТОЧНЫЙ"""
#     #     # Создаем заголовки без авторизации
#     #     headers_without_auth = {
#     #         "Accept": "application/json, text/plain, */*",
#     #         "Accept-Language": "en-US,en;q=0.9",
#     #         "Content-Type": "application/json"
#     #     }
#     #     
#     #     response = CategoriesAPI.get_categories_list(headers=headers_without_auth)
#     #     
#     #     # Проверяем, что запрос отклонен (401 или 403)
#     #     assert response.status_code in [401, 403], f"Ожидался статус 401 или 403, но получен {response.status_code}"
#     #     
#     #     print(f"Запрос без авторизации отклонен. Статус: {response.status_code}")
    
#     # def test_get_categories_list_response_time(self):
#     #     """Тест времени ответа списка категорий - ИЗБЫТОЧНЫЙ"""
#     #     start_time = time.time()
#     #     response = CategoriesAPI.get_categories_list()
#     #     response_time = (time.time() - start_time) * 1000
#     #     
#     #     # Проверяем статус код
#     #     assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #     
#     #     # Проверяем время ответа
#     #     Checking.check_response_time(response, MAX_CATEGORY_RESPONSE_TIME)
#     #     
#     #     print(f"Время ответа списка категорий: {response_time:.2f}ms")
    
#     # def test_get_categories_list_with_search(self):
#     #     """Тест получения списка категорий с поиском - ИЗБЫТОЧНЫЙ"""
#     #     for search_param in CATEGORY_SEARCH_PARAMS:
#     #         params = {'search': search_param}
#     #         response = CategoriesAPI.get_categories_list(params)
#     #         
#     #         # Проверяем статус код
#     #         assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
#     #         
#     #         # Проверяем данные
#     #         json_data = response.json()
#     #         assert json_data['success'] is True, "Операция должна быть успешной"
#     #         
#     #         print(f"Поиск по '{search_param}': найдено {len(json_data['data'])} элементов")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_category_basic.py 