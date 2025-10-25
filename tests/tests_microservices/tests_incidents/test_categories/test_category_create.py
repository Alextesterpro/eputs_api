# import pytest
# import time
# from tests_microservices.utils.incidents.categories_api import CategoriesAPI
# from tests_microservices.utils.incidents.categories_schemas import (
#     VALID_CATEGORY_DATA, 
#     MINIMAL_CATEGORY_DATA,
#     CATEGORY_RESPONSE_SCHEMA,
#     CATEGORY_DATA_SCHEMA,
#     CATEGORY_STATUS_CODES,
#     MAX_CATEGORY_RESPONSE_TIME
# )
# from tests_microservices.checking import Checking

# # Глобальная переменная для хранения ID созданных категорий
# created_category_ids = []

# @pytest.mark.detailed
# @pytest.mark.regression
# class TestCategoryCreate:
#     """Тесты создания категорий (рисков) - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

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
    
#     # def test_create_category_with_full_data(self):
#     #     """Тест создания категории с полными данными - ДУБЛИКАТ с basic"""
#     #     pass

#     # def test_create_category_with_minimal_data(self):
#     #     """Тест создания категории с минимальными данными - ИЗБЫТОЧНЫЙ"""
#     #     pass

#     # def test_create_category_with_special_characters(self):
#     #     """Тест создания категории со специальными символами - ИЗБЫТОЧНЫЙ"""
#     #     pass

#     # def test_create_category_with_long_names(self):
#     #     """Тест создания категории с длинными названиями - ИЗБЫТОЧНЫЙ"""
#     #     pass

#     # def test_create_category_with_numbers(self):
#     #     """Тест создания категории с числами - ИЗБЫТОЧНЫЙ"""
#     #     pass

#     # def test_create_category_with_unicode(self):
#     #     """Тест создания категории с Unicode - ИЗБЫТОЧНЫЙ"""
#     #     pass

#     # def test_create_multiple_categories(self):
#     #     """Тест создания множественных категорий - ИЗБЫТОЧНЫЙ"""
#     #     pass

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_category_basic.py 