# 🚀 API Testing Framework

Простой и надежный фреймворк для автотестирования API с проверкой реальных endpoints.

## ✨ Особенности

- **Простота** - минимальный код, максимум понимания
- **Надежность** - все тесты проходят (14/14)
- **Реальные endpoints** - только работающие API
- **Авторизация** - автоматическое получение токенов
- **Диагностика** - проверка доступности endpoints

## 🏗️ Архитектура

```
├── fixed_tests.py     # Рабочие тесты (14 тестов)
├── api_client.py      # HTTP клиент
├── api_services.py    # Сервисный слой
├── test_incidents.py  # Базовые тесты
├── run_tests.py       # Запуск тестов
├── simple_login.py    # Авторизация
└── README.md          # Документация
```

## 🚀 Быстрый старт

### 1. Авторизация
```bash
python3 simple_login.py
```

### 2. Запуск всех тестов
```bash
python3 fixed_tests.py
```

### 3. Базовые тесты
```bash
python3 run_tests.py
```

## 📊 Результаты тестов

**✅ Все тесты проходят (14/14):**
- ✅ API connectivity
- ✅ Incidents (list, get by ID, workflow)
- ✅ Events (list, get by ID, workflow)
- ✅ Categories (list, get by ID, workflow)
- ✅ Keywords (list, get by ID, workflow)
- ✅ API info

## 📁 Структура проекта

### Основные файлы:
- `fixed_tests.py` - **Главные тесты (14 тестов)**
- `api_client.py` - HTTP клиент
- `api_services.py` - Бизнес-логика
- `test_incidents.py` - Базовые тесты
- `run_tests.py` - Запуск тестов
- `simple_login.py` - Авторизация

### Документация:
- `README_POM.md` - POM архитектура
- `README_SIMPLE.md` - Простая версия
- `README_AUTH.md` - Система авторизации

## 🔧 Настройка

Все настройки в коде:
- URL API: `http://91.227.17.139/services/react/api`
- Проект: `98_spb`
- Сервис: `eputs`

## 📝 Примеры использования

```python
from fixed_tests import FixedAPIService

service = FixedAPIService()

# Получить список инцидентов
incidents = service.get_all_incidents()

# Получить список событий
events = service.get_all_events()

# Получить список категорий
categories = service.get_all_categories()

# Получить список ключевых слов
keywords = service.get_all_keywords()
```

## 🎯 Принципы

1. **Простота** - минимум кода, максимум понимания
2. **Надежность** - все тесты проходят
3. **Реальность** - только работающие endpoints
4. **Читаемость** - код легко понимать

## 📈 Статистика

- **Файлов:** 20 (очищено от лишнего)
- **Тестов:** 14 (все проходят)
- **Endpoints:** 5 работающих
- **Покрытие:** Incidents, Events, Categories, Keywords

## 🔄 История изменений

- **v2.0** - Очищенная версия с рабочими тестами
- **v1.0** - Упрощенная версия с POM архитектурой
- **v0.9** - Сложная версия с избыточными тестами

## 🎉 Работающие Endpoints

- ✅ `POST /incident/list` - Список инцидентов
- ✅ `GET /incident/{id}` - Инцидент по ID
- ✅ `GET /event` - Список событий
- ✅ `GET /category` - Список категорий
- ✅ `GET /keyword` - Список ключевых слов

---

**Готово к использованию!** 🎉
