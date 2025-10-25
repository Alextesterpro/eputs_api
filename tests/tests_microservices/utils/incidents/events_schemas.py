from typing import Dict, Any, List
from datetime import datetime

# Схемы ответов API мероприятий
EVENT_RESPONSE_SCHEMA = {
    'success': bool,
    'data': dict
}

EVENT_DATA_SCHEMA = {
    'id': int,
    'name': str,
    'short_name': str,
    'international_name': str,
    'date_start': str,
    'date_end': str,
    'project': str,
    'created_by': str,
    'updated_by': str,
    'created_at': str,
    'updated_at': str,
    'deleted_by': str,
    'deleted_at': str
}

EVENT_LIST_SCHEMA = {
    'data': list,
    'links': dict,
    'meta': dict,
    'success': bool
}

EVENT_OBJECT_SCHEMA = {
    'id': int,
    'name': str,
    'type_id': int,
    'type_name': str
}

# Примеры тестовых данных для мероприятий
VALID_EVENT_DATA = {
    "name": "Мероприятие 235",
    "short_name": "Мероприятие134",
    "international_name": "Events142",
    "date_start": "2025-08-01T09:34:59+03:00",
    "date_end": "2025-08-30T09:35:03+03:00",
    "objects": [
        {
            "id": 27,
            "project": "98_spb",
            "name": "ДИТ_155",
            "description": "А-121 \"Сортавала\" Санкт-Петербург - Сортавала - автомобильная дорога Р-21 \"Кола\". \nУчасток: 4 очередь: км 36+000 – км 57+550",
            "type_id": 69,
            "type": {
                "id": 69,
                "project": "98_spb",
                "name": "ДИТ",
                "created_by": None,
                "updated_by": None,
                "created_at": "2025-03-31T15:03:57.000000Z",
                "updated_at": "2025-03-31T15:03:57.000000Z"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [30.195523, 60.497795]
            },
            "organization_id": 0,
            "is_subscribe": False,
            "organization": {
                "id": 0,
                "title": "Организация по умолчанию",
                "project": "98_spb",
                "phones": [],
                "emails": [],
                "inn": "0000000000000",
                "juristic_address_id": None,
                "mail_address_id": None,
                "real_address_id": None,
                "created_by": None,
                "updated_by": None,
                "deleted_by": None,
                "deleted_at": None,
                "created_at": "2024-08-28T09:32:38.000000Z",
                "updated_at": "2024-08-28T09:32:38.000000Z",
                "full_name": "Организация по умолчанию",
                "attachments": [],
                "source": 1,
                "juristic_address": None,
                "mail_address": None,
                "real_address": None,
                "persons": []
            },
            "lat": "60.497795",
            "lon": "30.195523",
            "address": [],
            "events": [],
            "repair_objects": [],
            "address_text": "км 50+038 (прямой-обратный ход)",
            "cadastre": None,
            "created_by": None,
            "updated_by": None,
            "deleted_by": None,
            "created_at": "2025-03-31T15:03:57.000000Z",
            "updated_at": "2025-03-31T15:03:57.000000Z",
            "deleted_at": None,
            "type_name": "ДИТ"
        }
    ]
}

MINIMAL_EVENT_DATA = {
    "name": "Тестовое мероприятие",
    "short_name": "Тест",
    "international_name": "Test Event",
    "date_start": "2025-01-01T00:00:00+03:00",
    "date_end": "2025-01-31T23:59:59+03:00",
    "objects": []
}

# Невалидные данные для негативных тестов
INVALID_EVENT_DATA_EMPTY_NAME = {
    "name": "",
    "short_name": "Тест",
    "international_name": "Test Event",
    "date_start": "2025-01-01T00:00:00+03:00",
    "date_end": "2025-01-31T23:59:59+03:00",
    "objects": []
}

INVALID_EVENT_DATA_WRONG_DATE_FORMAT = {
    "name": "Тестовое мероприятие",
    "short_name": "Тест",
    "international_name": "Test Event",
    "date_start": "2025-01-01",  # Неправильный формат даты
    "date_end": "2025-01-31",    # Неправильный формат даты
    "objects": []
}

INVALID_EVENT_DATA_END_BEFORE_START = {
    "name": "Тестовое мероприятие",
    "short_name": "Тест",
    "international_name": "Test Event",
    "date_start": "2025-01-31T23:59:59+03:00",
    "date_end": "2025-01-01T00:00:00+03:00",  # Конец раньше начала
    "objects": []
}

# Статус коды
EVENT_STATUS_CODES = {
    'OK': 200,
    'CREATED': 201,
    'NOT_FOUND': 404,
    'VALIDATION_ERROR': 422,
    'UNAUTHORIZED': 401,
    'BAD_REQUEST': 400
}

# Форматы дат
EVENT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EVENT_DATE_FORMAT_ALT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Максимальное время ответа (мс)
MAX_EVENT_RESPONSE_TIME = 2000

# Параметры по умолчанию
DEFAULT_EVENT_PAGE = 1
DEFAULT_EVENT_LIMIT = 25
MAX_EVENT_LIMIT = 100 