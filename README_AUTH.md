# Система аутентификации для тестов

## Обзор

Реализована система управления токенами по лучшим практикам для API тестирования.

## Структура

```
config/
├── auth.py              # Основная система аутентификации
├── config.py            # Общие настройки
tests/
└── tests_microservices/
    └── utils/
        └── incidents/
            └── incidents_api.py  # API клиент с новой аутентификацией
```

## Приоритет загрузки токена

1. **Переменная окружения** `EPUTS_TOKEN` (высший приоритет)
2. **Конфигурационный файл** `config/auth.py` (дефолтный токен)
3. **Автоматическое обновление** (если реализовано)

## Использование

### 1. Через переменную окружения (рекомендуется для CI/CD)

```bash
export EPUTS_TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..."
python -m pytest tests/tests_microservices/tests_incidents/
```

### 2. Через файл .env (для локальной разработки)

```bash
# Скопируйте env.example в .env
cp env.example .env

# Отредактируйте .env
EPUTS_TOKEN=your_actual_token_here
```

### 3. Программно

```python
from config.auth import auth_manager

# Установить токен вручную
auth_manager.token_manager.set_token("new_token", expires_in_hours=24)

# Получить заголовки
headers = auth_manager.get_headers()
```

## Автоматическое обновление токена

Система автоматически:
- Проверяет срок действия токена
- Обновляет токен за 5 минут до истечения
- Использует переменную окружения если доступна

## Безопасность

- Токены НЕ коммитятся в git
- Файл `.env` исключен из .gitignore
- Дефолтный токен только для разработки
- В продакшене использовать переменные окружения

## Примеры

### Базовое использование

```python
from tests.tests_microservices.utils.incidents.incidents_api import IncidentsAPI

# API автоматически использует правильные заголовки
response = IncidentsAPI.get_incident(2)
```

### Кастомные заголовки

```python
extra_headers = {"X-Custom-Header": "value"}
response = IncidentsAPI.get_incident(2, headers=extra_headers)
```

### Проверка токена

```python
from config.auth import auth_manager

# Проверить текущий токен
token = auth_manager.token_manager.get_token()
print(f"Current token: {token[:50]}...")
```

## Миграция существующих тестов

Замените прямые импорты на использование новой системы:

```python
# Было
from tests_microservices.utils.incidents.incidents_api import IncidentsAPI

# Стало (то же самое, но с новой аутентификацией)
from tests.tests_microservices.utils.incidents.incidents_api import IncidentsAPI
```

## Troubleshooting

### 401 Unauthorized
- Проверьте переменную `EPUTS_TOKEN`
- Убедитесь что токен не истек
- Проверьте права доступа

### Import errors
- Убедитесь что `config/` в PYTHONPATH
- Проверьте структуру импортов

### Токен не обновляется
- Проверьте логи
- Убедитесь что auth endpoint доступен
