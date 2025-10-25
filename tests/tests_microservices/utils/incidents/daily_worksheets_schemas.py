from typing import Dict, Any, List
from datetime import datetime, date, timedelta

# Схемы ответов API ведомостей
WORKSHEET_RESPONSE_SCHEMA = {
    'data': dict
}

WORKSHEET_DATA_SCHEMA = {
    'id': int,
    'date': str,
    'project': str,
    'created_by': str,
    'updated_by': str,
    'created_at': str,
    'updated_at': str,
    'success': bool
}

WORKSHEET_LIST_SCHEMA = {
    'data': list,
    'links': dict,
    'meta': dict,
    'success': bool
}

# Примеры тестовых данных для ведомостей
VALID_WORKSHEET_DATA = {
    "date": "2025-01-27"
}

MINIMAL_WORKSHEET_DATA = {
    "date": "2025-01-28"
}

# Невалидные данные для негативных тестов
INVALID_WORKSHEET_DATA_EMPTY_DATE = {
    "date": ""
}

INVALID_WORKSHEET_DATA_NO_DATE = {
    "name": "Ведомость без даты"
}

INVALID_WORKSHEET_DATA_INVALID_DATE_FORMAT = {
    "date": "2025/01/27"
}

INVALID_WORKSHEET_DATA_PAST_DATE = {
    "date": "2020-01-01"
}

INVALID_WORKSHEET_DATA_FUTURE_DATE = {
    "date": "2030-01-01"
}

# Статус коды
WORKSHEET_STATUS_CODES = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'VALIDATION_ERROR': 422,
    'UNAUTHORIZED': 401,
    'BAD_REQUEST': 400,
    'CONFLICT': 409,
    'FORBIDDEN': 403
}

# Максимальное время ответа (мс)
MAX_WORKSHEET_RESPONSE_TIME = 2000

# Параметры по умолчанию
DEFAULT_WORKSHEET_PAGE = 1
DEFAULT_WORKSHEET_LIMIT = 25
MAX_WORKSHEET_LIMIT = 100

# Примеры реальных данных из cURL
REAL_WORKSHEET_DATA = {
    "date": "2025-08-06"
}

# Параметры поиска
WORKSHEET_SEARCH_PARAMS = {
    'page': 1,
    'limit': 25,
    'date': '2025-01-27'
}

# Различные форматы дат для тестирования
DATE_FORMATS = [
    "2025-01-27",
    "2025-01-28", 
    "2025-02-01",
    "2025-12-31"
]

# Граничные значения дат
BOUNDARY_DATES = {
    'today': date.today().strftime("%Y-%m-%d"),
    'yesterday': (date.today() - timedelta(days=1)).strftime("%Y-%m-%d"),
    'tomorrow': (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
    'min_date': "2020-01-01",
    'max_date': "2030-12-31"
} 