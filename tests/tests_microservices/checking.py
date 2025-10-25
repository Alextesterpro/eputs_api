import json
from requests import Response
import logging
from typing import Any, List, Dict, Union
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class Checking:
    @staticmethod
    def check_status_code(response: Response, status_code: int) -> None:
        """Проверка статус кода ответа"""
        assert response.status_code == status_code, \
            f"Ожидался статус {status_code}, но получен {response.status_code}. Ответ:\n{response.text}"
        logging.info(f"Успешно! Статус код: {response.status_code}")

    @staticmethod
    def check_json_token(response: Response, expected_keys: List[str]) -> None:
        """Проверка наличия ожидаемых ключей в JSON ответе"""
        try:
            response_json = response.json()
        except json.JSONDecodeError as e:
            raise AssertionError(f"Ответ не является валидным JSON: {e}. Ответ: {response.text}")

        missing_keys = [key for key in expected_keys if key not in response_json]
        if missing_keys:
            raise AssertionError(f"Отсутствуют ключи: {missing_keys}. Ответ: {response_json}")

        logging.info("Все ключи присутствуют.")

    @staticmethod
    def check_json_value(response: Response, key: str, expected_value: Any) -> None:
        """Проверка конкретного значения в JSON ответе"""
        value = response.json().get(key)
        assert value == expected_value, \
            f"Ожидалось значение {expected_value} для поля {key}, но получено {value}"
        logging.info(f"Значение поля {key} верно!")

    @staticmethod
    def check_json_schema(response: Response, schema: Dict[str, Any]) -> None:
        """Проверка соответствия JSON ответа схеме"""
        response_json = response.json()
        for key, expected_type in schema.items():
            if key in response_json:
                actual_type = type(response_json[key])
                assert actual_type == expected_type, \
                    f"Тип поля {key} должен быть {expected_type}, но получен {actual_type}"

    @staticmethod
    def check_response_time(response: Response, max_time_ms: int) -> None:
        """Проверка времени ответа"""
        response_time = response.elapsed.total_seconds() * 1000
        assert response_time <= max_time_ms, \
            f"Время ответа {response_time}ms превышает максимально допустимое {max_time_ms}ms"

    @staticmethod
    def check_date_format(response: Response, date_field: str, expected_format: str) -> None:
        """Проверка формата даты в ответе"""
        date_str = response.json().get(date_field)
        try:
            datetime.strptime(date_str, expected_format)
        except ValueError:
            raise AssertionError(f"Дата {date_str} не соответствует формату {expected_format}")

    @staticmethod
    def check_list_length(response: Response, list_field: str, min_length: int = 0, max_length: int = None) -> None:
        """Проверка длины списка в ответе"""
        items = response.json().get(list_field, [])
        length = len(items)
        assert length >= min_length, f"Длина списка {list_field} меньше минимальной ({min_length})"
        if max_length is not None:
            assert length <= max_length, f"Длина списка {list_field} больше максимальной ({max_length})"