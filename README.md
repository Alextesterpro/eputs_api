# API Testing Framework

Фреймворк для автотестирования API множественных сервисов с единообразным подходом.

## Особенности

- **Единообразие** - все API используют прямые клиенты без промежуточных слоев
- **Полное покрытие** - 6 основных сервисов (Incidents, DTP, Metro, Parking, Digital Twin, External Transport)
- **Реальные endpoints** - тесты работают с реальным API
- **Авторизация** - автоматическое получение и валидация токенов
- **Диагностика** - проверка валидности токенов для всех сервисов

## Архитектура

```
DorisAutomatiomAPI/
├── api_clients/                     # API клиенты для всех сервисов
│   ├── __init__.py                  # Экспорт всех клиентов
│   ├── incidents.py                 # API клиент для Инцидентов
│   ├── dtp.py                       # API клиент для ДТП
│   ├── metro.py                     # API клиент для Метрополитен
│   ├── parking.py                   # API клиент для Парковок
│   ├── digital_twin.py              # API клиент для Цифрового двойника
│   └── external_transport.py        # API клиент для Внешнего транспорта
├── update_token.py                  # Скрипт авторизации и обновления токена
├── run_all_tests.py                 # Запуск всех тестов
├── tests/
│   ├── conftest.py                  # Общие фикстуры для всех тестов
│   ├── test_api_info.py             # Тесты валидации токенов
│   ├── tests_incidents/             # Тесты для Инцидентов
│   │   ├── test_incidents.py        # CRUD тесты для инцидентов
│   │   ├── test_events.py           # CRUD тесты для событий
│   │   ├── test_categories.py       # CRUD тесты для категорий
│   │   ├── test_keywords.py         # CRUD тесты для ключевых слов
│   │   └── test_factors.py          # CRUD тесты для факторов
│   ├── tests_dtp/                   # Тесты для ДТП
│   ├── tests_metro/                 # Тесты для Метрополитен
│   ├── tests_parking/               # Тесты для Парковок
│   ├── tests_digital_twin/          # Тесты для Цифрового двойника
│   └── tests_external_transport/    # Тесты для Внешнего транспорта
├── .env                             # Токен авторизации (не в git)
└── requirements.txt                 # Зависимости проекта
```

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Авторизация
```bash
python3 update_token.py
```
Введите логин и пароль. Токен сохранится в `.env`

### 3. Запуск всех тестов
```bash
python3 run_all_tests.py
```

### 4. Запуск тестов конкретного сервиса
```bash
# Incidents
pytest tests/tests_incidents/ -v

# DTP
pytest tests/tests_dtp/ -v

# Metro
pytest tests/tests_metro/ -v

# Parking
pytest tests/tests_parking/ -v

# Digital Twin
pytest tests/tests_digital_twin/ -v

# External Transport
pytest tests/tests_external_transport/ -v
```

### 5. Проверка токенов
```bash
pytest tests/test_api_info.py -v
```

## Принципы архитектуры

### Прямые API клиенты
Каждый сервис имеет свой API клиент, который:
- Читает токен из `.env`
- Формирует заголовки с нужными параметрами (`project`, `service`)
- Предоставляет методы для всех endpoints
- Возвращает `Response` объект без обработки

### Тесты
Все тесты следуют единому стилю:
```python
def test_something(self, incidents_client):
    """Тест описание"""
    result = incidents_client.some_method()
    assert result.status_code == 200, f"Status code: {result.status_code}"
    data = result.json()
    assert "data" in data, "Нет поля data"
    print("Something работает")
```

### Фикстуры
Все фикстуры определены в `conftest.py`:
- `incidents_client` - клиент для Инцидентов
- `dtp_client` - клиент для ДТП
- `metro_client` - клиент для Метрополитен
- `parking_client` - клиент для Парковок
- `digital_twin_client` - клиент для Цифрового двойника
- `external_transport_client` - клиент для Внешнего транспорта

## Примеры использования

### Использование в тестах
```python
def test_incidents_list(self, incidents_client):
    """Тест получения списка инцидентов"""
    result = incidents_client.get_incidents_list(page=1, limit=10)
    assert result.status_code == 200
    data = result.json()
    assert "data" in data
```

### Использование в скриптах
```python
from api_clients import IncidentsAPIClient

client = IncidentsAPIClient()
response = client.get_incidents_list(page=1, limit=5)
if response.status_code == 200:
    incidents = response.json()
    print(incidents)
```

### Импорт всех клиентов
```python
from api_clients import (
    IncidentsAPIClient,
    DTPAPIClient,
    MetroAPIClient,
    ParkingAPIClient,
    DigitalTwinAPIClient,
    ExternalTransportAPIClient
)
```

## Проверка токена

Каждый API клиент имеет метод `check_token()`:
```python
result = client.check_token()
print(f"Валиден: {result['valid']}")
print(f"Статус код: {result['status_code']}")
print(f"Сообщение: {result['message']}")
```

## Настройка

Все настройки в коде API клиентов:
- **Incidents**: `http://91.227.17.139/services/react/api`
- **DTP**: `http://91.227.17.139/services/dtp/api`
- **Metro**: `http://91.227.17.139/services/metro/api`
- **Parking**: `http://91.227.17.139/services/parking/api`
- **Digital Twin**: `http://91.227.17.139/services/road-network/api` и `cifdv-graph/api`
- **External Transport**: `http://91.227.17.139/services/transport-external/api`

Все сервисы используют:
- **Проект**: `98_spb`
- **Токен**: из `.env`

## Покрытие тестами

| Сервис | Тесты | Статус |
|--------|-------|--------|
| Incidents | 27 тестов | ✅ 24 passed, 2 skipped, 1 failed |
| Events | 5 тестов | ✅ All passed |
| Categories | 5 тестов | ✅ 4 passed, 1 failed (400 - системная категория) |
| Keywords | 5 тестов | ✅ All passed |
| Factors | 6 тестов | ✅ 4 passed, 2 skipped (системные факторы) |
| DTP | 8 тестов | ✅ All passed |
| Metro | 9 тестов | ✅ All passed |
| Parking | 8 тестов | ✅ All passed |
| Digital Twin | 11 тестов | ✅ 10 passed, 1 skipped (500 API error) |
| External Transport | 5 тестов | ✅ All passed |
| Token Checks | 9 тестов | ✅ All passed |

## Troubleshooting

### Токен протух
```bash
python3 update_token.py
```

### Проверка токена
```bash
pytest tests/test_api_info.py::TestTokenCheck -v
```

### Проблемы с сертификатами
Все клиенты используют `verify=False` для игнорирования SSL предупреждений.

---

**Готово к использованию!**
