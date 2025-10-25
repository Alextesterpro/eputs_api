# API Тесты - POM Architecture

## 🏗️ Архитектура проекта

Проект следует принципам **Page Object Model (POM)** и лучшим практикам автотестирования API:

```
├── api_client.py      # Слой API клиента
├── api_models.py      # Модели данных
├── api_services.py    # Сервисный слой
├── test_incidents.py  # Тесты
├── run_tests.py       # Запуск тестов
├── simple_login.py    # Авторизация
└── .env               # Токен
```

## 🔧 Слои архитектуры

### 1. API Client (`api_client.py`)
- **Назначение**: Низкоуровневые HTTP запросы
- **Принципы**: Инкапсуляция HTTP логики
- **Методы**: `get_incidents_list()`, `create_incident()`, etc.

### 2. Models (`api_models.py`)
- **Назначение**: Модели данных и валидация
- **Принципы**: Типизация, валидация
- **Классы**: `Incident`, `IncidentListResponse`, `APIResponse`

### 3. Services (`api_services.py`)
- **Назначение**: Бизнес-логика и обработка данных
- **Принципы**: Абстракция, обработка ошибок
- **Методы**: `get_all_incidents()`, `create_incident()`, etc.

### 4. Tests (`test_incidents.py`)
- **Назначение**: Тестовые сценарии
- **Принципы**: AAA (Arrange-Act-Assert), изоляция
- **Классы**: `TestIncidentAPI`, `TestIncidentAPIEdgeCases`

## 🚀 Быстрый старт

### 1. Авторизация
```bash
python3 simple_login.py
```

### 2. Запуск тестов
```bash
python3 run_tests.py
```

### 3. Запуск с отчетом
```bash
python3 -m pytest test_incidents.py --html=report.html
```

## 📋 Тестовые сценарии

### Основные тесты
- ✅ Проверка доступности API
- ✅ Получение списка инцидентов
- ✅ Получение инцидента по ID
- ✅ Поиск инцидентов
- ✅ Создание инцидента
- ✅ Обновление инцидента
- ✅ Удаление инцидента
- ✅ Полный workflow

### Граничные случаи
- ✅ Несуществующий инцидент
- ✅ Пустые данные
- ✅ Пагинация
- ✅ Обработка ошибок

## 🎯 Принципы POM

### 1. Инкапсуляция
- Каждый слой скрывает детали реализации
- API Client скрывает HTTP детали
- Services скрывают бизнес-логику

### 2. Абстракция
- Тесты работают с высокоуровневыми методами
- Не зависят от HTTP деталей
- Легко читаются и понимаются

### 3. Переиспользование
- API Client переиспользуется в разных тестах
- Models используются везде
- Services инкапсулируют общую логику

### 4. Поддерживаемость
- Изменения в API затрагивают только Client
- Тесты не зависят от реализации
- Легко добавлять новые тесты

## 🔍 Лучшие практики

### 1. AAA Pattern
```python
def test_create_incident(self):
    # Arrange
    name = "Тест"
    description = "Описание"
    
    # Act
    result = self.service.create_incident(name, description)
    
    # Assert
    assert result.name == name
```

### 2. Изоляция тестов
- Каждый тест независим
- Используются фикстуры для настройки
- Очистка после тестов

### 3. Обработка ошибок
- Проверка статус кодов
- Валидация ответов
- Обработка исключений

### 4. Типизация
- Использование type hints
- Валидация данных
- Четкие интерфейсы

## 📊 Отчеты

Тесты генерируют HTML отчеты с:
- Статистикой выполнения
- Детальной информацией об ошибках
- Временем выполнения
- Покрытием тестами

## 🛠️ Настройка

Все настройки в коде:
- URL API: `http://91.227.17.139/services/react/api`
- Проект: `98_spb`
- Сервис: `eputs`
- Токен: автоматически из `.env`

## 📝 Примеры использования

```python
from api_services import IncidentService

service = IncidentService()

# Получить список
incidents = service.get_all_incidents(page=1, limit=10)

# Создать инцидент
new_incident = service.create_incident("Название", "Описание")

# Обновить
updated = service.update_incident(1, description="Новое описание")

# Удалить
service.delete_incident(1)
```
