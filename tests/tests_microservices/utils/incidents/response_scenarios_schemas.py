from typing import Dict, Any, List

# Схемы ответов API сценариев реагирования
SCENARIO_RESPONSE_SCHEMA = {
    'data': dict
}

SCENARIO_DATA_SCHEMA = {
    'id': int,
    'name': str,
    'project': str,
    'created_by': str,
    'updated_by': str,
    'created_at': str,
    'updated_at': str,
    'success': bool
}

SCENARIO_LIST_SCHEMA = {
    'data': list,
    'links': dict,
    'meta': dict,
    'success': bool
}

# Минимальные тестовые данные для сценария
MINIMAL_SCENARIO_DATA = {
    "name": "Тестовый сценарий реагирования 2025",
    "operation_list": [
        {
            "position": 1,
            "is_typical": True,
            "name": "Ознакомиться с описанием инцидента[ЦУТ]",
            "type": 1,
            "operation_id": 1,
            "organization_id": 3,  # Используем реальный ID организации ЦУТ
            "cycle": "",
            "time": 10,
            "is_auto": False,
            "is_transfer": False,
            "is_parallel": False,
            "parallel": [],
            "group": None,
            "is_send_ext_system": True,
            "ext_system_id": 2,
            "ext_system_text": "Тестовое"
        }
    ],
    "event_id": 4,  # Используем реальный ID события
    "keyword_id_list": [164],  # Используем реальный ID ключевого слова
    "event_object_id_list": [],
    "is_typical": True,
    "attachments": [],
    "comment": "Тестовый комментарий",
    "types": [{"id": 111}],
    "factors": []
}

# Полные тестовые данные для сценария
VALID_SCENARIO_DATA = {
    "name": "Полный сценарий реагирования 2025",
    "operation_list": [
        {
            "position": 1,
            "is_typical": True,
            "name": "Ознакомиться с описанием инцидента[ЦУТ]",
            "type": 1,
            "operation_id": 1,
            "organization_id": 3,  # Используем реальный ID организации ЦУТ
            "cycle": "",
            "time": 10,
            "is_auto": False,
            "is_transfer": False,
            "is_parallel": False,
            "parallel": [],
            "group": None,
            "is_send_ext_system": True,
            "ext_system_id": 2,
            "ext_system_text": "Тестовое"
        }
    ],
    "event": {
        "id": 4,
        "name": "Мониторинг дорог",
        "short_name": "Мониторинг дорог",
        "international_name": "",
        "date_start": "2017-04-22T00:00:00+00:00",
        "date_end": "2017-04-22T00:00:00+00:00",
        "project": "98_spb"
    },
    "event_id": 4,  # Используем реальный ID события
    "category": None,
    "category_id": None,
    "keyword_list": [
        {
            "id": 164,
            "name": "Россия",
            "project": "98_spb"
        }
    ],
    "keyword_id_list": [184],
    "event_object_list": [],
    "event_object_id_list": [],
    "is_typical": True,
    "attachments": [],
    "comment": "Коммет",
    "types": [{"id": 111}],
    "factors": [{"id": 41}]
}

# Невалидные данные для негативных тестов
INVALID_SCENARIO_DATA_EMPTY_NAME = {
    "name": "",
    "operation_list": [],
    "event_id": 1
}

INVALID_SCENARIO_DATA_NO_NAME = {
    "operation_list": [],
    "event_id": 1
}

INVALID_SCENARIO_DATA_NO_OPERATIONS = {
    "name": "Сценарий без операций",
    "event_id": 1
}

INVALID_SCENARIO_DATA_NO_EVENT = {
    "name": "Сценарий без события",
    "operation_list": []
}

# Статус коды
SCENARIO_STATUS_CODES = {
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
MAX_SCENARIO_RESPONSE_TIME = 3000

# Параметры по умолчанию
DEFAULT_SCENARIO_PAGE = 1
DEFAULT_SCENARIO_LIMIT = 25
MAX_SCENARIO_LIMIT = 100

# Параметры поиска
SCENARIO_SEARCH_PARAMS = {
    'page': 1,
    'limit': 25,
    'name': 'сценарий'
}

# Данные для обновления сценария
UPDATE_SCENARIO_DATA = {
    "name": "Обновленный сценарий реагирования 2025",
    "operation_list": [
        {
            "response_scenario_id": 192,
            "operation_id": 1,
            "position": 1,
            "organization_id": 2,
            "cycle": "",
            "is_parallel": False,
            "parallel": [],
            "time": 10,
            "is_auto": False,
            "is_transfer": False,
            "is_typical": True,
            "type": 1,
            "group": None,
            "is_send_ext_system": True,
            "ext_system_id": 2,
            "ext_system_text": "Тестовое",
            "is_auto_next": False,
            "regulation_at": "[\"00:10:00\"]",
            "name": "Ознакомиться с описанием инцидента[ЦУТ]"
        }
    ],
    "event": {
        "id": 2,
        "name": "Второй матч Зенит - Терек",
        "short_name": "Зенит - Терек",
        "international_name": "",
        "date_start": "2017-05-07T00:00:00+00:00",
        "date_end": "2017-05-07T00:00:00+00:00",
        "project": "98_spb"
    },
    "event_id": 2,
    "category": None,
    "category_id": None,
    "keyword_list": [
        {
            "id": 184,
            "name": "Подвижной состав",
            "project": "98_spb"
        }
    ],
    "keyword_id_list": [184],
    "event_object_list": [],
    "event_object_id_list": [],
    "is_typical": True,
    "attachments": [],
    "comment": "Обновленный комментарий",
    "types": [{"id": 111}],
    "factors": [{"id": 41}]
}

# Данные для копирования сценария
COPY_SCENARIO_DATA = {
    "name": "Копия сценария реагирования 2025",
    "operation_list": [
        {
            "response_scenario_id": 192,
            "operation_id": 1,
            "position": 1,
            "organization_id": 2,
            "cycle": "",
            "is_parallel": False,
            "parallel": [],
            "time": 10,
            "is_auto": False,
            "is_transfer": False,
            "is_typical": True,
            "type": 1,
            "group": None,
            "is_send_ext_system": True,
            "ext_system_id": 2,
            "ext_system_text": "Тестовое",
            "is_auto_next": False,
            "regulation_at": "[\"00:10:00\"]",
            "name": "Ознакомиться с описанием инцидента[ЦУТ]"
        }
    ],
    "event": {
        "id": 2,
        "name": "Второй матч Зенит - Терек",
        "short_name": "Зенит - Терек",
        "international_name": "",
        "date_start": "2017-05-07T00:00:00+00:00",
        "date_end": "2017-05-07T00:00:00+00:00",
        "project": "98_spb"
    },
    "event_id": 2,
    "category": None,
    "category_id": None,
    "keyword_list": [
        {
            "id": 184,
            "name": "Подвижной состав",
            "project": "98_spb"
        }
    ],
    "keyword_id_list": [184],
    "event_object_list": [],
    "event_object_id_list": [],
    "is_typical": True,
    "attachments": [],
    "comment": "Коммет",
    "types": [{"id": 111}],
    "factors": [{"id": 41}]
} 