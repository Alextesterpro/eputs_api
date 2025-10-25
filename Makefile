# Makefile для запуска тестов API мероприятий

.PHONY: help smoke basic detailed negative performance real-data regression all install clean

# По умолчанию показываем справку
help:
	@echo "Доступные команды:"
	@echo "  make smoke      - Запустить smoke тесты (быстрая проверка)"
	@echo "  make basic      - Запустить базовые тесты"
	@echo "  make detailed   - Запустить детальные тесты"
	@echo "  make negative   - Запустить негативные тесты"
	@echo "  make performance - Запустить тесты производительности"
	@echo "  make real-data  - Запустить тесты с реальными данными"
	@echo "  make regression - Запустить регрессионные тесты"
	@echo "  make all        - Запустить все тесты"
	@echo "  make install    - Установить зависимости"
	@echo "  make clean      - Очистить кэш pytest"

# Smoke тесты - быстрая проверка
smoke:
	@echo "Запуск smoke тестов..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m smoke -v --tb=short

# Базовые тесты
basic:
	@echo "Запуск базовых тестов..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m basic -v --tb=short

# Детальные тесты
detailed:
	@echo "Запуск детальных тестов..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m detailed -v --tb=short

# Негативные тесты
negative:
	@echo "Запуск негативных тестов..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m negative -v --tb=short

# Тесты производительности
performance:
	@echo "Запуск тестов производительности..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m performance -v --tb=short

# Тесты с реальными данными
real-data:
	@echo "Запуск тестов с реальными данными..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m real_data -v --tb=short

# Регрессионные тесты
regression:
	@echo "Запуск регрессионных тестов..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -m regression -v --tb=short

# Все тесты
all:
	@echo "Запуск всех тестов..."
	python3 -m pytest tests/tests_microservices/tests_incidents/test_events/ -v --tb=short

# Установка зависимостей
install:
	@echo "Установка зависимостей..."
	pip install -r requirements.txt

# Очистка кэша
clean:
	@echo "Очистка кэша pytest..."
	python3 -m pytest --cache-clear
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true 