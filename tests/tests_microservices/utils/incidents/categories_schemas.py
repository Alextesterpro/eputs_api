from typing import Dict, Any, List

# Схемы ответов API категорий
CATEGORY_RESPONSE_SCHEMA = {
    'data': dict
}

CATEGORY_DATA_SCHEMA = {
    'id': int,
    'name': str,
    'project': str,
    'created_by': str,
    'updated_by': str,
    'created_at': str,
    'updated_at': str,
    'success': bool
}

CATEGORY_LIST_SCHEMA = {
    'data': list,
    'links': dict,
    'meta': dict,
    'success': bool
}

# Примеры тестовых данных для категорий
VALID_CATEGORY_DATA = {
    "name": "Тестовая категория риска 2025"
}

MINIMAL_CATEGORY_DATA = {
    "name": "Минимальная категория 2025"
}

# Невалидные данные для негативных тестов
INVALID_CATEGORY_DATA_EMPTY_NAME = {
    "name": ""
}

INVALID_CATEGORY_DATA_NO_NAME = {
    "description": "Категория без названия"
}

INVALID_CATEGORY_DATA_LONG_NAME = {
    "name": "Очень длинное название категории риска которое превышает допустимые ограничения системы и может вызвать проблемы с валидацией данных на стороне сервера"
}

# Статус коды
CATEGORY_STATUS_CODES = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'VALIDATION_ERROR': 422,
    'UNAUTHORIZED': 401,
    'BAD_REQUEST': 400,
    'CONFLICT': 409
}

# Максимальное время ответа (мс)
MAX_CATEGORY_RESPONSE_TIME = 2000

# Параметры по умолчанию
DEFAULT_CATEGORY_PAGE = 1
DEFAULT_CATEGORY_LIMIT = 25
MAX_CATEGORY_LIMIT = 100

# Примеры реальных данных из cURL
REAL_CATEGORY_DATA = {
    "name": "Добавление123"
}

# Параметры поиска
CATEGORY_SEARCH_PARAMS = {
    'page': 1,
    'limit': 25,
    'name': 'название'
} 