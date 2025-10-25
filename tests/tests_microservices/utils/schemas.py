from typing import Dict, Any, List
from datetime import datetime

# Схемы ответов API
API_RESPONSE_SCHEMA = {
    'success': bool,
    'data': dict,
    'is_auth': bool
}

TRANSPORT_LIST_SCHEMA = {
    'data': list,
    'links': dict,
    'meta': dict,
    'success': bool,
    'is_auth': bool
}

# Схема ответа для сгруппированных маршрутов
GROUPED_ROUTES_SCHEMA = {
    'data': list,
    'links': dict,
    'meta': dict,
    'success': bool,
    'is_auth': bool
}

# Схема ответа для версии API
VERSION_SCHEMA = {
    'version': str,
    'build_date': str,
    'git_commit': str,
    'git_branch': str
}

# Параметры по умолчанию
DEFAULT_PAGE = 1
DEFAULT_LIMIT = 25
MAX_LIMIT = 100

# Форматы дат
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

# Максимальное время ответа (мс)
MAX_RESPONSE_TIME = 1000

# Коды ответов
STATUS_CODES = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'VALIDATION_ERROR': 422,
    'UNAUTHORIZED': 401
}

# Типы транспорта
TRANSPORT_TYPES = {
    'BUS': 1,
    'TRAM': 2,
    'TROLLEYBUS': 3
}

# Типы связи
COMMUNICATION_TYPES = {
    'GSM': 1,
    'GPS': 2,
    'GLONASS': 3
}

# Статусы транспорта
TRANSPORT_STATUSES = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'MAINTENANCE': 3,
    'REPAIR': 4
}

# Типы топлива
FUEL_TYPES = {
    'DIESEL': 1,
    'GASOLINE': 2,
    'ELECTRIC': 3,
    'HYBRID': 4
}

# Статусы маршрутов
ROUTE_STATUSES = {
    'ACTIVE': 1,
    'INACTIVE': 2,
    'MAINTENANCE': 3,
    'REPAIR': 4
}

# Примеры тестовых данных
TEST_TRANSPORT_DATA = {
    'name': 'Test Bus',
    'model': 'Test Model',
    'carnum': 'A123BC',
    'serial': '123456789',
    'caption': 'Test Caption',
    'conditioning': 'Yes',
    'bicycle_racks': 'Yes',
    'places_for_strollers': 'Yes',
    'low_floor': 'Yes',
    'wc': 'No',
    'organization_id': 1,
    'route_num': '10a',
    'class_id': 1,
    'transport_type': TRANSPORT_TYPES['BUS'],
    'communication_type': COMMUNICATION_TYPES['GSM'],
    'status': TRANSPORT_STATUSES['ACTIVE'],
    'fuel_type': FUEL_TYPES['DIESEL']
}

# Валидационные правила
VALIDATION_RULES = {
    'carnum': r'^[A-Z]\d{3}[A-Z]{2}$',  # Формат: A123BC
    'phone': r'^7\d{10}$',  # Формат: 79221234567
    'number_sim': r'^\d{10}$',  # Формат: 1234567890
    'route_num': r'^[0-9]+[a-z]?$'  # Формат: 10 или 10a
}

# Схема ответа для создания маршрута
ROUTE_CREATE_SCHEMA = {
    'data': {
        'id': int,
        'category_id': int,
        'group_num': str,
        'group_order': int,
        'created_at': str,
        'updated_at': str
    },
    'success': bool,
    'is_auth': bool
}

# Категории маршрутов
ROUTE_CATEGORIES = {
    'BUS': 1,
    'TRAM': 2,
    'TROLLEYBUS': 3
}

# Примеры тестовых данных для маршрутов
TEST_ROUTE_DATA = {
    'category_id': ROUTE_CATEGORIES['BUS'],
    'group_num': '123 А',
    'group_order': 1
} 