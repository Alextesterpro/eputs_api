# import pytest
# import uuid
# from datetime import date, timedelta
# from tests_microservices.utils.incidents.daily_worksheets_api import DailyWorksheetsAPI
# from tests_microservices.utils.incidents.daily_worksheets_schemas import (
#     WORKSHEET_STATUS_CODES,
#     MAX_WORKSHEET_RESPONSE_TIME,
#     DATE_FORMATS,
#     BOUNDARY_DATES
# )
# from tests_microservices.checking import Checking

# # Глобальная переменная для хранения ID созданных ведомостей
# created_worksheet_ids = []
# import time

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
# class TestWorksheetCreate:
#     """Тесты создания ежедневных ведомостей - ИЗБЫТОЧНЫЕ ТЕСТЫ"""

#     # def teardown_method(self):
#     #     """Очистка после каждого теста - удаление созданных ведомостей"""
#     #     global created_worksheet_ids
#     #     for worksheet_id in created_worksheet_ids:
#     #         try:
#     #             DailyWorksheetsAPI.delete_worksheet(worksheet_id)
#     #             print(f"Удалена ведомость с ID: {worksheet_id}")
#     #         except Exception as e:
#     #             print(f"Ошибка при удалении ведомости {worksheet_id}: {e}")
#     #     created_worksheet_ids.clear()

#     # def test_create_worksheet_with_today_date(self):
#     #     """Тест создания ведомости с сегодняшней датой - ИЗБЫТОЧНЫЙ"""
#     #     # Тест создания с сегодняшней датой
#     #     pass

#     # def test_create_worksheet_with_yesterday_date(self):
#     #     """Тест создания ведомости со вчерашней датой - ИЗБЫТОЧНЫЙ"""
#     #     # Тест создания со вчерашней датой
#     #     pass

#     # def test_create_worksheet_with_tomorrow_date(self):
#     #     """Тест создания ведомости с завтрашней датой - ИЗБЫТОЧНЫЙ"""
#     #     # Тест создания с завтрашней датой
#     #     pass

#     # @pytest.mark.parametrize("date_format", DATE_FORMATS)
#     # def test_create_worksheet_with_different_date_formats(self, date_format):
#     #     """Тест создания ведомости с разными форматами дат - ИЗБЫТОЧНЫЙ"""
#     #     # Тест с разными форматами дат
#     #     pass

#     # def test_create_multiple_worksheets(self):
#     #     """Тест создания множественных ведомостей - ИЗБЫТОЧНЫЙ"""
#     #     # Тест создания нескольких ведомостей
#     #     pass

#     # def test_create_worksheet_response_time(self):
#     #     """Тест времени ответа создания ведомости - ИЗБЫТОЧНЫЙ"""
#     #     # Тест времени ответа
#     #     pass

#     # def test_create_worksheet_with_special_characters_in_date(self):
#     #     """Тест создания ведомости со спецсимволами в дате - ИЗБЫТОЧНЫЙ"""
#     #     # Тест со спецсимволами
#     #     pass

#     # def test_create_worksheet_with_long_date(self):
#     #     """Тест создания ведомости с длинной датой - ИЗБЫТОЧНЫЙ"""
#     #     # Тест с длинной датой
#     #     pass

#     # def test_create_worksheet_with_numbers_in_date(self):
#     #     """Тест создания ведомости с числовыми значениями в дате"""
#     #     unique_data = get_unique_worksheet_data({"date": "2025-01-27"})
        
#     #     response = DailyWorksheetsAPI.create_worksheet(unique_data)
        
#     #     assert response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]], \
#     #         f"Ожидался статус 201 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
#     #     print("Создание ведомости с числовыми значениями в дате работает корректно")

#     # def test_create_worksheet_with_unicode_date(self):
#     #     """Тест создания ведомости с Unicode символами в дате"""
#     #     # Этот тест должен провалиться
#     #     test_data = {"date": "2025-01-27\u00A0"}  # неразрывный пробел
        
#     #     response = DailyWorksheetsAPI.create_worksheet(test_data)
        
#     #     # Ожидаем ошибку валидации
#     #     assert response.status_code in [WORKSHEET_STATUS_CODES["VALIDATION_ERROR"], WORKSHEET_STATUS_CODES["BAD_REQUEST"]], \
#     #         f"Ожидался статус 422 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
#     #     print("Валидация Unicode символов в дате работает корректно")

#     # def test_create_worksheet_with_duplicate_date(self):
#     #     """Тест создания ведомости с дублирующейся датой"""
#     #     # Создаем первую ведомость
#     #     test_data = {"date": "2025-01-27"}
#     #     response1 = DailyWorksheetsAPI.create_worksheet(test_data)
        
#     #     if response1.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]]:
#     #         # Пытаемся создать вторую ведомость с той же датой
#     #         response2 = DailyWorksheetsAPI.create_worksheet(test_data)
            
#     #         # Проверяем, что вторая ведомость не создалась (конфликт или валидация)
#     #         assert response2.status_code in [
#     #             WORKSHEET_STATUS_CODES["CONFLICT"], 
#     #             WORKSHEET_STATUS_CODES["VALIDATION_ERROR"], 
#     #             WORKSHEET_STATUS_CODES["BAD_REQUEST"]
#     #         ], f"Ожидался статус 409, 422 или 400, но получен {response2.status_code}. Ответ: {response2.text}"
            
#     #         print("Валидация дублирующихся дат работает корректно")
#     #     else:
#     #         print("Первая ведомость не была создана, пропускаем тест дублирования")

#     # def test_create_worksheet_with_boundary_dates(self):
#     #     """Тест создания ведомости с граничными датами"""
#     #     boundary_tests = [
#     #         ("min_date", BOUNDARY_DATES['min_date']),
#     #         ("max_date", BOUNDARY_DATES['max_date'])
#     #     ]
        
#     #     for test_name, test_date in boundary_tests:
#     #         unique_id = str(uuid.uuid4())[:8]
#     #         modified_date = f"{test_date[:-2]}{unique_id[-2:]}"
#     #         test_data = {"date": modified_date}
            
#     #         response = DailyWorksheetsAPI.create_worksheet(test_data)
            
#     #         # API может вернуть ошибку валидации или сервера
#     #         assert response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"], WORKSHEET_STATUS_CODES["BAD_REQUEST"], WORKSHEET_STATUS_CODES["VALIDATION_ERROR"]], \
#     #             f"Ожидался статус 201, 200, 400 или 422 для {test_name}, но получен {response.status_code}. Ответ: {response.text}"
            
#     #         if response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]]:
#     #             print(f"Ведомость с граничной датой {test_name} создана: {modified_date}")
#     #         else:
#     #             print(f"Серверная ошибка при создании ведомости с граничной датой {test_name}: {response.status_code}") 

# # ВСЕ ТЕСТЫ В ЭТОМ ФАЙЛЕ ЗАКОММЕНТИРОВАНЫ КАК ИЗБЫТОЧНЫЕ
# # Основная функциональность покрывается в test_worksheet_basic.py 