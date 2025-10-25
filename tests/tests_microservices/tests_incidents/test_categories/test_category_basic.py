import pytest
import time
import uuid
from tests_microservices.utils.incidents.categories_api import CategoriesAPI
from tests_microservices.utils.incidents.categories_schemas import (
    VALID_CATEGORY_DATA, 
    MINIMAL_CATEGORY_DATA,
    INVALID_CATEGORY_DATA_EMPTY_NAME,
    INVALID_CATEGORY_DATA_NO_NAME,
    INVALID_CATEGORY_DATA_LONG_NAME,
    CATEGORY_RESPONSE_SCHEMA,
    CATEGORY_DATA_SCHEMA,
    CATEGORY_STATUS_CODES,
    MAX_CATEGORY_RESPONSE_TIME
)
from tests_microservices.checking import Checking

# Глобальная переменная для хранения ID созданных категорий
created_category_ids = []

def get_unique_category_data(base_data):
    """Генерирует уникальные данные для категории"""
    unique_id = str(uuid.uuid4())[:8]
    unique_data = base_data.copy()
    unique_data['name'] = f"{base_data['name']} {unique_id}"
    return unique_data

@pytest.mark.basic
@pytest.mark.smoke
@pytest.mark.regression
class TestCategoriesBasic:
    """Базовые тесты для категорий (рисков)"""

    def teardown_method(self):
        """Очистка после каждого теста - удаление созданных категорий"""
        global created_category_ids
        for category_id in created_category_ids:
            try:
                CategoriesAPI.delete_category(category_id)
                print(f"Удалена категория с ID: {category_id}")
            except Exception as e:
                print(f"Ошибка при удалении категории {category_id}: {e}")
        created_category_ids.clear()
    
    @pytest.mark.smoke
    def test_create_category(self):
        """Тест создания категории"""
        unique_data = get_unique_category_data(VALID_CATEGORY_DATA)
        response = CategoriesAPI.create_category(unique_data)
        
        # Проверяем статус код
        assert response.status_code in (CATEGORY_STATUS_CODES["CREATED"], CATEGORY_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
        
        # Проверяем структуру ответа
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        
        # Проверяем данные категории
        assert json_data['success'] is True, "Операция должна быть успешной"
        category_data = json_data['data']
        assert category_data['name'] == unique_data['name'], "Название должно совпадать"
        assert 'id' in category_data, "Должен быть ID категории"
        
        # Сохраняем ID для последующего удаления
        created_category_ids.append(category_data['id'])
        
        print(f"Категория создана успешно. ID: {category_data['id']}")
    
    @pytest.mark.smoke
    def test_get_categories_list(self):
        """Тест получения списка категорий"""
        response = CategoriesAPI.get_categories_list()
        
        # Проверяем статус код
        assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
        
        # Проверяем структуру ответа
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert isinstance(json_data['data'], list), "Данные должны быть списком"
        
        print(f"Получен список категорий. Количество: {len(json_data['data'])}")
    
    @pytest.mark.smoke
    def test_get_category_by_id(self):
        """Тест получения категории по ID"""
        # Сначала создаем категорию
        unique_data = get_unique_category_data(MINIMAL_CATEGORY_DATA)
        create_response = CategoriesAPI.create_category(unique_data)
        assert create_response.status_code in (CATEGORY_STATUS_CODES["CREATED"], CATEGORY_STATUS_CODES["OK"])
        
        category_id = create_response.json()['data']['id']
        created_category_ids.append(category_id)
        
        # Получаем категорию по ID
        response = CategoriesAPI.get_category_by_id(category_id)
        
        # Проверяем статус код
        assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
        
        # Проверяем данные
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert json_data['success'] is True, "Операция должна быть успешной"
        assert json_data['data']['id'] == category_id, "ID должен совпадать"
        assert json_data['data']['name'] == unique_data['name'], "Название должно совпадать"
        
        print(f"Категория получена по ID: {category_id}")
    
    @pytest.mark.smoke
    def test_update_category(self):
        """Тест обновления категории"""
        # Сначала создаем категорию
        unique_data = get_unique_category_data(MINIMAL_CATEGORY_DATA)
        create_response = CategoriesAPI.create_category(unique_data)
        assert create_response.status_code in (CATEGORY_STATUS_CODES["CREATED"], CATEGORY_STATUS_CODES["OK"])
        
        category_id = create_response.json()['data']['id']
        created_category_ids.append(category_id)
        
        # Обновляем категорию
        update_data = {"name": f"Обновленное название категории {str(uuid.uuid4())[:8]}"}
        response = CategoriesAPI.update_category(category_id, update_data)
        
        # Проверяем статус код
        assert response.status_code == CATEGORY_STATUS_CODES["OK"], f"Ожидался статус 200, но получен {response.status_code}"
        
        # Проверяем данные
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert json_data['success'] is True, "Операция должна быть успешной"
        assert json_data['data']['name'] == update_data['name'], "Название должно обновиться"
        
        print(f"Категория обновлена. ID: {category_id}")
    
    @pytest.mark.smoke
    def test_delete_category(self):
        """Тест удаления категории"""
        # Сначала создаем категорию
        unique_data = get_unique_category_data(MINIMAL_CATEGORY_DATA)
        create_response = CategoriesAPI.create_category(unique_data)
        assert create_response.status_code in (CATEGORY_STATUS_CODES["CREATED"], CATEGORY_STATUS_CODES["OK"])
        
        category_id = create_response.json()['data']['id']
        created_category_ids.append(category_id)
        
        # Удаляем категорию
        response = CategoriesAPI.delete_category(category_id)
        
        # Проверяем статус код
        assert response.status_code in (CATEGORY_STATUS_CODES["OK"], CATEGORY_STATUS_CODES["NOT_FOUND"]), f"Ожидался статус 200 или 404, но получен {response.status_code}"
        
        # Проверяем, что категория действительно удалена
        get_response = CategoriesAPI.get_category_by_id(category_id)
        assert get_response.status_code == CATEGORY_STATUS_CODES["NOT_FOUND"], "Категория должна быть удалена"
        
        print(f"Категория удалена. ID: {category_id}")
    
    def test_create_category_with_full_data(self):
        """Тест создания категории с полными данными"""
        start_time = time.time()
        unique_data = get_unique_category_data(VALID_CATEGORY_DATA)
        response = CategoriesAPI.create_category(unique_data)
        response_time = (time.time() - start_time) * 1000
        
        # Проверяем статус код
        assert response.status_code in (CATEGORY_STATUS_CODES["CREATED"], CATEGORY_STATUS_CODES["OK"]), f"Ожидался статус 201 или 200, но получен {response.status_code}"
        
        # Проверяем время ответа
        assert response_time < MAX_CATEGORY_RESPONSE_TIME, f"Время ответа {response_time:.2f}ms превышает лимит {MAX_CATEGORY_RESPONSE_TIME}ms"
        
        # Проверяем структуру ответа
        json_data = response.json()
        Checking.check_json_token(response, ['data'])
        
        # Проверяем данные категории
        assert json_data['success'] is True, "Операция должна быть успешной"
        category_data = json_data['data']
        assert category_data['name'] == unique_data['name'], "Название должно совпадать"
        assert 'id' in category_data, "Должен быть ID категории"
        assert isinstance(category_data['id'], int), "ID должен быть числом"
        
        # Сохраняем ID для последующего удаления
        created_category_ids.append(category_data['id'])
        
        # Проверяем схему данных
        Checking.check_json_schema(response, CATEGORY_DATA_SCHEMA)
        
        print(f"Категория создана успешно. ID: {category_data['id']}, Время ответа: {response_time:.2f}ms")
    
    def test_invalid_category_id(self):
        """Тест работы с невалидным ID категории"""
        invalid_ids = [0, -1, 999999]
        
        for invalid_id in invalid_ids:
            response = CategoriesAPI.get_category_by_id(invalid_id)
            
            # Проверяем, что получаем ошибку
            assert response.status_code in (CATEGORY_STATUS_CODES["NOT_FOUND"], CATEGORY_STATUS_CODES["BAD_REQUEST"]), \
                f"Неожиданный статус код {response.status_code} для ID {invalid_id}"
            
            print(f"Корректно обработана ошибка для невалидного ID {invalid_id}")
    
    def test_empty_category_name(self):
        """Тест создания категории с пустым названием"""
        response = CategoriesAPI.create_category(INVALID_CATEGORY_DATA_EMPTY_NAME)
        
        # Проверяем статус код ошибки
        assert response.status_code in (CATEGORY_STATUS_CODES["VALIDATION_ERROR"], CATEGORY_STATUS_CODES["BAD_REQUEST"]), \
            f"Ожидался статус 422 или 400, но получен {response.status_code}"
        
        print("Корректно обработана ошибка для пустого названия")
    
    def test_category_without_name(self):
        """Тест создания категории без названия"""
        response = CategoriesAPI.create_category(INVALID_CATEGORY_DATA_NO_NAME)
        
        # Проверяем статус код ошибки
        assert response.status_code in (CATEGORY_STATUS_CODES["VALIDATION_ERROR"], CATEGORY_STATUS_CODES["BAD_REQUEST"]), \
            f"Ожидался статус 422 или 400, но получен {response.status_code}"
        
        print("Корректно обработана ошибка для категории без названия")
    
    def test_category_with_long_name(self):
        """Тест создания категории с очень длинным названием"""
        response = CategoriesAPI.create_category(INVALID_CATEGORY_DATA_LONG_NAME)
        
        # Проверяем статус код (может быть ошибка или успех в зависимости от ограничений)
        assert response.status_code in (CATEGORY_STATUS_CODES["CREATED"], CATEGORY_STATUS_CODES["OK"], 
                                       CATEGORY_STATUS_CODES["VALIDATION_ERROR"], CATEGORY_STATUS_CODES["BAD_REQUEST"]), \
            f"Неожиданный статус код {response.status_code}"
        
        print("Проверена обработка длинного названия категории") 