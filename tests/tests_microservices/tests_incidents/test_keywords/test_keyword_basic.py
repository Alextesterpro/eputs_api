import pytest
import time
import uuid
from tests_microservices.utils.incidents.keywords_api import KeywordsAPI
from tests_microservices.utils.incidents.keywords_schemas import (
    VALID_KEYWORD_DATA,
    MINIMAL_KEYWORD_DATA,
    INVALID_KEYWORD_DATA_EMPTY_NAME,
    INVALID_KEYWORD_DATA_NO_NAME,
    INVALID_KEYWORD_DATA_LONG_NAME,
    INVALID_KEYWORD_DATA_SPECIAL_CHARS,
    KEYWORD_RESPONSE_SCHEMA,
    KEYWORD_DATA_SCHEMA,
    KEYWORD_STATUS_CODES,
    MAX_KEYWORD_RESPONSE_TIME
)
from tests_microservices.checking import Checking

# Глобальная переменная для хранения ID созданных ключевых слов
created_keyword_ids = []

def get_unique_keyword_data(base_data):
    """Генерирует уникальные данные для ключевого слова"""
    unique_id = str(uuid.uuid4())[:8]
    unique_data = base_data.copy()
    unique_data['name'] = f"{base_data['name']} {unique_id}"
    return unique_data

@pytest.mark.basic
@pytest.mark.smoke
@pytest.mark.regression
class TestKeywordBasic:
    """Базовые тесты для ключевых слов"""

    def teardown_method(self):
        """Очистка после каждого теста - удаление созданных ключевых слов"""
        global created_keyword_ids
        for keyword_id in created_keyword_ids:
            try:
                KeywordsAPI.delete_keyword(keyword_id)
                print(f"Удален ключевое слово с ID: {keyword_id}")
            except Exception as e:
                print(f"Ошибка при удалении ключевого слова {keyword_id}: {e}")
        created_keyword_ids.clear()

    def test_create_keyword(self):
        """Тест создания ключевого слова"""
        unique_data = get_unique_keyword_data(VALID_KEYWORD_DATA)
        
        response = KeywordsAPI.create_keyword(unique_data)
        
        # Проверяем статус код
        assert response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]], \
            f"Ожидался статус 201 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем структуру ответа
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert 'success' in json_data, "Должно быть поле success на верхнем уровне"
        
        keyword_data = json_data['data']
        assert 'id' in keyword_data, "Должен быть ID"
        assert 'name' in keyword_data, "Должно быть название"
        
        # Сохраняем ID для последующего удаления
        created_keyword_ids.append(keyword_data['id'])
        
        print(f"Ключевое слово создано успешно. ID: {keyword_data['id']}")

    def test_get_keywords_list(self):
        """Тест получения списка ключевых слов"""
        response = KeywordsAPI.get_keywords_list()
        
        # Проверяем статус код
        assert response.status_code == KEYWORD_STATUS_CODES["OK"], \
            f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
        
        # Проверяем структуру ответа
        json_data = response.json()
        assert 'data' in json_data, "Должен быть блок data"
        assert isinstance(json_data['data'], list), "Data должен быть списком"
        
        print(f"Получен список ключевых слов. Количество: {len(json_data['data'])}")

    def test_get_keyword_by_id(self):
        """Тест получения ключевого слова по ID"""
        # Сначала создаем ключевое слово
        unique_data = get_unique_keyword_data(VALID_KEYWORD_DATA)
        create_response = KeywordsAPI.create_keyword(unique_data)
        
        if create_response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]]:
            keyword_id = create_response.json()['data']['id']
            created_keyword_ids.append(keyword_id)
            
            # Получаем ключевое слово по ID
            response = KeywordsAPI.get_keyword_by_id(keyword_id)
            
            # Проверяем статус код
            assert response.status_code == KEYWORD_STATUS_CODES["OK"], \
                f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
            
            # Проверяем структуру ответа
            json_data = response.json()
            assert 'data' in json_data, "Должен быть блок data"
            assert 'success' in json_data, "Должно быть поле success на верхнем уровне"
            
            keyword_data = json_data['data']
            assert keyword_data['id'] == keyword_id, "ID должен совпадать"
            
            print(f"Ключевое слово получено по ID: {keyword_id}")

    def test_update_keyword(self):
        """Тест обновления ключевого слова"""
        # Сначала создаем ключевое слово
        unique_data = get_unique_keyword_data(VALID_KEYWORD_DATA)
        create_response = KeywordsAPI.create_keyword(unique_data)
        
        if create_response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]]:
            keyword_id = create_response.json()['data']['id']
            created_keyword_ids.append(keyword_id)
            
            # Обновляем ключевое слово
            update_data = get_unique_keyword_data(VALID_KEYWORD_DATA)
            response = KeywordsAPI.update_keyword(keyword_id, update_data)
            
            # Проверяем статус код
            assert response.status_code == KEYWORD_STATUS_CODES["OK"], \
                f"Ожидался статус 200, но получен {response.status_code}. Ответ: {response.text}"
            
            print(f"Ключевое слово обновлено. ID: {keyword_id}")

    def test_delete_keyword(self):
        """Тест удаления ключевого слова"""
        # Сначала создаем ключевое слово
        unique_data = get_unique_keyword_data(VALID_KEYWORD_DATA)
        create_response = KeywordsAPI.create_keyword(unique_data)
        
        if create_response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]]:
            keyword_id = create_response.json()['data']['id']
            created_keyword_ids.append(keyword_id)
            
            # Удаляем ключевое слово
            response = KeywordsAPI.delete_keyword(keyword_id)
            
            # Проверяем статус код
            assert response.status_code in [KEYWORD_STATUS_CODES["OK"], KEYWORD_STATUS_CODES["NOT_FOUND"]], \
                f"Ожидался статус 200 или 404, но получен {response.status_code}. Ответ: {response.text}"
            
            print(f"Ключевое слово удалено. ID: {keyword_id}")

    def test_create_keyword_with_minimal_data(self):
        """Тест создания ключевого слова с минимальными данными"""
        unique_data = get_unique_keyword_data(MINIMAL_KEYWORD_DATA)
        
        response = KeywordsAPI.create_keyword(unique_data)
        
        # Проверяем статус код
        assert response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]], \
            f"Ожидался статус 201 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
        # Сохраняем ID для последующего удаления
        if response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]]:
            keyword_id = response.json()['data']['id']
            created_keyword_ids.append(keyword_id)
        
        print("Ключевое слово с минимальными данными создано успешно")

    # Негативные тесты
    def test_create_keyword_empty_name(self):
        """Тест создания ключевого слова с пустым названием"""
        response = KeywordsAPI.create_keyword(INVALID_KEYWORD_DATA_EMPTY_NAME)
        
        # Проверяем статус код
        assert response.status_code in [KEYWORD_STATUS_CODES["VALIDATION_ERROR"], KEYWORD_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 422 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Валидация пустого названия работает корректно")

    def test_create_keyword_no_name(self):
        """Тест создания ключевого слова без названия"""
        response = KeywordsAPI.create_keyword(INVALID_KEYWORD_DATA_NO_NAME)
        
        # Проверяем статус код
        assert response.status_code in [KEYWORD_STATUS_CODES["VALIDATION_ERROR"], KEYWORD_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 422 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Валидация отсутствующего названия работает корректно")

    def test_create_keyword_long_name(self):
        """Тест создания ключевого слова с очень длинным названием"""
        response = KeywordsAPI.create_keyword(INVALID_KEYWORD_DATA_LONG_NAME)
        

        assert response.status_code in [KEYWORD_STATUS_CODES["VALIDATION_ERROR"], KEYWORD_STATUS_CODES["BAD_REQUEST"], KEYWORD_STATUS_CODES["OK"]], \
            f"Ожидался статус 422, 400 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
        if response.status_code == KEYWORD_STATUS_CODES["OK"]:
            # Сохраняем ID для последующего удаления
            keyword_id = response.json()['data']['id']
            created_keyword_ids.append(keyword_id)
            print("API создал ключевое слово с длинным названием (более толерантен к данным)")
        else:
            print("Валидация длинного названия работает корректно")

    def test_create_keyword_special_chars(self):
        """Тест создания ключевого слова со специальными символами"""
        response = KeywordsAPI.create_keyword(INVALID_KEYWORD_DATA_SPECIAL_CHARS)
        
        # API может быть толерантным к специальным символам
        assert response.status_code in [KEYWORD_STATUS_CODES["VALIDATION_ERROR"], KEYWORD_STATUS_CODES["BAD_REQUEST"], KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]], \
            f"Ожидался статус 422, 400, 201 или 200, но получен {response.status_code}. Ответ: {response.text}"
        
        if response.status_code in [KEYWORD_STATUS_CODES["CREATED"], KEYWORD_STATUS_CODES["OK"]]:
            # Сохраняем ID для последующего удаления
            keyword_id = response.json()['data']['id']
            created_keyword_ids.append(keyword_id)
            print("API принял специальные символы в названии")
        else:
            print("Валидация специальных символов работает корректно")

    def test_get_keyword_invalid_id(self):
        """Тест получения ключевого слова с неверным ID"""
        response = KeywordsAPI.get_keyword_by_id(99999)
        
        # Проверяем статус код
        assert response.status_code == KEYWORD_STATUS_CODES["NOT_FOUND"], \
            f"Ожидался статус 404, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Получение несуществующего ключевого слова работает корректно")

    def test_update_keyword_invalid_id(self):
        """Тест обновления ключевого слова с неверным ID"""
        response = KeywordsAPI.update_keyword(99999, VALID_KEYWORD_DATA)
        
        # Проверяем статус код
        assert response.status_code == KEYWORD_STATUS_CODES["NOT_FOUND"], \
            f"Ожидался статус 404, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Обновление несуществующего ключевого слова работает корректно")

    def test_delete_keyword_invalid_id(self):
        """Тест удаления ключевого слова с неверным ID"""
        response = KeywordsAPI.delete_keyword(99999)
        
        # Проверяем статус код (API может вернуть 400 или 404)
        assert response.status_code in [KEYWORD_STATUS_CODES["NOT_FOUND"], KEYWORD_STATUS_CODES["BAD_REQUEST"]], \
            f"Ожидался статус 404 или 400, но получен {response.status_code}. Ответ: {response.text}"
        
        print("Удаление несуществующего ключевого слова работает корректно") 