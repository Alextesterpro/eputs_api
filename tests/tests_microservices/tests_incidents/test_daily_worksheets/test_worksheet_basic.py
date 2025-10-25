import pytest
import time
import uuid
from datetime import date
from tests_microservices.utils.incidents.daily_worksheets_api import DailyWorksheetsAPI
from tests_microservices.utils.incidents.daily_worksheets_schemas import (
    VALID_WORKSHEET_DATA,
    MINIMAL_WORKSHEET_DATA,
    INVALID_WORKSHEET_DATA_EMPTY_DATE,
    INVALID_WORKSHEET_DATA_NO_DATE,
    INVALID_WORKSHEET_DATA_INVALID_DATE_FORMAT,
    WORKSHEET_RESPONSE_SCHEMA,
    WORKSHEET_DATA_SCHEMA,
    WORKSHEET_STATUS_CODES,
    MAX_WORKSHEET_RESPONSE_TIME
)
from tests_microservices.checking import Checking

# Глобальная переменная для хранения ID созданных ведомостей
created_worksheet_ids = []

def get_unique_worksheet_data(base_data):
    """Генерирует уникальные данные для ведомости"""
    unique_id = str(uuid.uuid4())[:8]
    unique_data = base_data.copy()
    # Создаем уникальную дату, добавляя случайные дни
    import random
    from datetime import datetime, timedelta
    
    base_date = datetime.strptime(base_data['date'], "%Y-%m-%d")
    random_days = random.randint(1, 365)  # Случайное количество дней
    unique_date = base_date + timedelta(days=random_days)
    unique_data['date'] = unique_date.strftime("%Y-%m-%d")
    return unique_data

@pytest.mark.basic
@pytest.mark.smoke
@pytest.mark.regression
class TestWorksheetBasic:
    """Базовые тесты для ежедневных рабочих ведомостей"""

    def teardown_method(self):
        """Очистка после каждого теста - удаление созданных ведомостей"""
        global created_worksheet_ids
        for worksheet_id in created_worksheet_ids:
            try:
                DailyWorksheetsAPI.delete_worksheet(worksheet_id)
                print(f"Удалена ведомость с ID: {worksheet_id}")
            except Exception as e:
                print(f"Ошибка при удалении ведомости {worksheet_id}: {e}")
        created_worksheet_ids.clear()

    def test_create_worksheet(self):
        """Тест создания ведомости"""
        unique_data = get_unique_worksheet_data(VALID_WORKSHEET_DATA)
        
        response = DailyWorksheetsAPI.create_worksheet(unique_data)
        
        # Проверяем статус код
        assert response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]], \
            f"Ожидался статус 201 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем структуру ответа
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert 'success' in json_data, "Должно быть поле success на верхнем уровне"
        
        worksheet_data = json_data['data']
        assert 'id' in worksheet_data, "Должен быть ID"
        assert 'date' in worksheet_data, "Должна быть дата"
        
        # Сохраняем ID для последующего удаления
        created_worksheet_ids.append(worksheet_data['id'])
        
        print(f"Ведомость создана успешно. ID: {worksheet_data['id']}")

    def test_get_worksheets_list(self):
        """Тест получения списка ведомостей"""
        response = DailyWorksheetsAPI.get_worksheets_list()
        
        # Проверяем статус код
        assert response.status_code == WORKSHEET_STATUS_CODES["OK"], \
            f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем структуру ответа
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert isinstance(json_data['data'], list), "Data должен быть списком"
        
        print(f"Получен список ведомостей. Количество: {len(json_data['data'])}")

    def test_get_worksheet_by_id(self):
        """Тест получения ведомости по ID"""
        # Сначала создаем ведомость
        unique_data = get_unique_worksheet_data(VALID_WORKSHEET_DATA)
        create_response = DailyWorksheetsAPI.create_worksheet(unique_data)
        
        if create_response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]]:
            worksheet_id = create_response.json()['data']['id']
            created_worksheet_ids.append(worksheet_id)
            
            # Получаем ведомость по ID
            response = DailyWorksheetsAPI.get_worksheet_by_id(worksheet_id)
            
            # Проверяем статус код
            assert response.status_code == WORKSHEET_STATUS_CODES["OK"], \
                f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
            
            # Проверяем структуру ответа
            json_data = response.json()
            assert 'data' in json_data, "Должен быть блок data"
            assert 'success' in json_data, "Должно быть поле success на верхнем уровне"
            
            worksheet_data = json_data['data']
            assert worksheet_data['id'] == worksheet_id, "ID должен совпадать"
            
            print(f"Ведомость получена по ID: {worksheet_id}")

    def test_delete_worksheet(self):
        """Тест удаления ведомости"""
        # Сначала создаем ведомость
        unique_data = get_unique_worksheet_data(VALID_WORKSHEET_DATA)
        create_response = DailyWorksheetsAPI.create_worksheet(unique_data)
        
        if create_response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]]:
            worksheet_id = create_response.json()['data']['id']
            created_worksheet_ids.append(worksheet_id)
            
            # Удаляем ведомость
            response = DailyWorksheetsAPI.delete_worksheet(worksheet_id)
            
            # Проверяем статус код
            assert response.status_code in [WORKSHEET_STATUS_CODES["OK"], WORKSHEET_STATUS_CODES["NOT_FOUND"]], \
                f"Ожидался статус 200 или 404, но получен {response.status_code}. Ответ: {response.text}"
            
            print(f"Ведомость удалена. ID: {worksheet_id}")

    def test_create_worksheet_with_minimal_data(self):
        """Тест создания ведомости с минимальными данными"""
        unique_data = get_unique_worksheet_data(MINIMAL_WORKSHEET_DATA)
        
        response = DailyWorksheetsAPI.create_worksheet(unique_data)
        
        # Проверяем статус код
        assert response.status_code in [WORKSHEET_STATUS_CODES["CREATED"], WORKSHEET_STATUS_CODES["OK"]], \
            f"Ожидался статус 201 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Ведомость с минимальными данными создана успешно")

    # Негативные тесты
    def test_create_worksheet_empty_date(self):
        """Тест создания ведомости с пустой датой"""
        response = DailyWorksheetsAPI.create_worksheet(INVALID_WORKSHEET_DATA_EMPTY_DATE)
        
        # Проверяем статус код
        assert response.status_code in [WORKSHEET_STATUS_CODES["VALIDATION_ERROR"], WORKSHEET_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 422 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Валидация пустой даты работает корректно")

    def test_create_worksheet_no_date(self):
        """Тест создания ведомости без даты"""
        response = DailyWorksheetsAPI.create_worksheet(INVALID_WORKSHEET_DATA_NO_DATE)
        
        # Проверяем статус код
        assert response.status_code in [WORKSHEET_STATUS_CODES["VALIDATION_ERROR"], WORKSHEET_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 422 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Валидация отсутствующей даты работает корректно")

    def test_create_worksheet_invalid_date_format(self):
        """Тест создания ведомости с неверным форматом даты"""
        response = DailyWorksheetsAPI.create_worksheet(INVALID_WORKSHEET_DATA_INVALID_DATE_FORMAT)
        
        # Проверяем статус код
        assert response.status_code in [WORKSHEET_STATUS_CODES["VALIDATION_ERROR"], WORKSHEET_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 422 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Валидация формата даты работает корректно")

    def test_get_worksheet_invalid_id(self):
        """Тест получения ведомости с неверным ID"""
        response = DailyWorksheetsAPI.get_worksheet_by_id(99999)
        
        # Проверяем статус код
        assert response.status_code == WORKSHEET_STATUS_CODES["NOT_FOUND"], \
            f"Ожидался статус 404, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Получение несуществующей ведомости работает корректно")

    def test_delete_worksheet_invalid_id(self):
        """Тест удаления ведомости с неверным ID"""
        response = DailyWorksheetsAPI.delete_worksheet(99999)
        
        # Проверяем статус код (API может вернуть 400 или 404)
        assert response.status_code in [WORKSHEET_STATUS_CODES["NOT_FOUND"], WORKSHEET_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 404 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Удаление несуществующей ведомости работает корректно") 