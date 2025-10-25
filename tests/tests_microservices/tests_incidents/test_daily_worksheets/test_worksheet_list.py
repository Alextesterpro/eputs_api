# import pytest
# import uuid
# from tests_microservices.utils.incidents.daily_worksheets_api import DailyWorksheetsAPI
# from tests_microservices.utils.incidents.daily_worksheets_schemas import (
#     WORKSHEET_STATUS_CODES,
#     WORKSHEET_SEARCH_PARAMS,
#     DEFAULT_WORKSHEET_PAGE,
#     DEFAULT_WORKSHEET_LIMIT,
#     MAX_WORKSHEET_LIMIT
# )
# from tests_microservices.checking import Checking

# Глобальная переменная для хранения ID созданных ведомостей
# created_worksheet_ids = []

# def get_unique_worksheet_data(base_data):
#     """Генерирует уникальные данные для ведомости"""
#     unique_id = str(uuid.uuid4())[:8]
#     unique_data = base_data.copy()
#     # Создаем уникальную дату, добавляя случайные дни
#     import random
#     from datetime import datetime, timedelta
    
#     base_date = datetime.strptime(base_data['date'], "%Y-%m-%d")
#     random_days = random.randint(1, 365)  # Случайное количество дней
#     unique_date = base_date + timedelta(days=random_days)
#     unique_data['date'] = unique_date.strftime("%Y-%m-%d")
#     return unique_data

# @pytest.mark.regression
# class TestWorksheetList:
#     """Тесты получения списка ежедневных ведомостей - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

#     # def test_get_worksheets_list_success(self):
#     #     """Тест успешного получения списка ведомостей - ДУБЛИКАТ с basic"""
#     #     response = DailyWorksheetsAPI.get_worksheets_list()
#     #     assert response.status_code == 200
#     #     print("Список ведомостей получен")

#     # def test_get_worksheets_list_with_pagination(self):
#     #     """Тест получения списка ведомостей с пагинацией - ИЗБЫТОЧНЫЙ"""
#     #     params = {'page': 1, 'limit': 10}
#     #     response = DailyWorksheetsAPI.get_worksheets_list(params)
#     #     assert response.status_code == 200
#     #     print("Список ведомостей с пагинацией получен")

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_worksheet_basic.py 