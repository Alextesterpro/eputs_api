# Простые тесты API инцидентов

## 🚀 Быстрый старт

### 1. Авторизация
```bash
python3 simple_login.py
```

### 2. Запуск тестов
```bash
python3 simple_tests.py
```

## 📁 Структура проекта

- `simple_login.py` - авторизация и получение токена
- `simple_api.py` - простой API клиент
- `simple_tests.py` - простые тесты
- `.env` - файл с токеном (создается автоматически)

## 🔧 Как это работает

1. **Авторизация**: Получаем токен и сохраняем в `.env`
2. **API клиент**: Простые функции для работы с API
3. **Тесты**: Проверяем основные операции

## 📋 Тесты

- ✅ Получение списка инцидентов
- ✅ Получение одного инцидента  
- ✅ Поиск инцидентов
- ✅ Создание инцидента

## 🛠️ Настройка

Все настройки в коде:
- URL API: `http://91.227.17.139/services/react/api`
- Проект: `98_spb`
- Сервис: `eputs`

## 📝 Примеры

```python
from simple_api import SimpleIncidentAPI

api = SimpleIncidentAPI()

# Получить список
response = api.list_incidents(page=1, limit=10)

# Получить один
response = api.get_incident(1)

# Создать
response = api.create_incident("Название", "Описание")
```
