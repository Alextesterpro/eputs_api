#!/usr/bin/env python3
"""
Скрипт для автоматического добавления очистки (teardown_method) во все тестовые файлы
"""

import os
import re
from pathlib import Path

def add_cleanup_to_test_file(file_path):
    """Добавляет очистку в тестовый файл"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Определяем тип API по пути к файлу
    if 'keywords' in str(file_path):
        api_class = 'KeywordsAPI'
        entity_name = 'ключевое слово'
        entity_var = 'keyword_id'
        created_ids_var = 'created_keyword_ids'
    elif 'scenarios' in str(file_path):
        api_class = 'ResponseScenariosAPI'
        entity_name = 'сценарий'
        entity_var = 'scenario_id'
        created_ids_var = 'created_scenario_ids'
    elif 'worksheets' in str(file_path):
        api_class = 'DailyWorksheetsAPI'
        entity_name = 'ведомость'
        entity_var = 'worksheet_id'
        created_ids_var = 'created_worksheet_ids'
    elif 'categories' in str(file_path):
        api_class = 'CategoriesAPI'
        entity_name = 'категория'
        entity_var = 'category_id'
        created_ids_var = 'created_category_ids'
    elif 'events' in str(file_path):
        api_class = 'EventsAPI'
        entity_name = 'событие'
        entity_var = 'event_id'
        created_ids_var = 'created_event_ids'
    else:
        print(f"Неизвестный тип API для файла: {file_path}")
        return False
    
    # Проверяем, есть ли уже очистка
    if 'teardown_method' in content:
        print(f"Очистка уже есть в файле: {file_path}")
        return False
    
    # Добавляем глобальную переменную для ID
    if created_ids_var not in content:
        # Находим место после импортов
        import_pattern = r'from tests_microservices\.checking import Checking'
        if import_pattern in content:
            content = content.replace(
                'from tests_microservices.checking import Checking',
                f'from tests_microservices.checking import Checking\n\n# Глобальная переменная для хранения ID созданных {entity_name}ей\n{created_ids_var} = []'
            )
    
    # Добавляем teardown_method в класс
    class_pattern = r'class Test\w+:\s*\n\s*"""[^"]*"""\s*\n'
    teardown_method = f'''    def teardown_method(self):
        """Очистка после каждого теста - удаление созданных {entity_name}ей"""
        global {created_ids_var}
        for {entity_var} in {created_ids_var}:
            try:
                {api_class}.delete_{entity_name.replace(' ', '_')}({entity_var})
                print(f"Удален {entity_name} с ID: {{{entity_var}}}")
            except Exception as e:
                print(f"Ошибка при удалении {entity_name}а {{{entity_var}}}: {{e}}")
        {created_ids_var}.clear()

'''
    
    # Заменяем начало класса
    content = re.sub(
        class_pattern,
        lambda m: m.group(0) + teardown_method,
        content
    )
    
    # Добавляем сохранение ID во все места создания
    create_pattern = r'(\s+)(\w+_id)\s*=\s*create_response\.json\(\)\[\'data\'\]\[\'id\'\]'
    replacement = r'\1\2 = create_response.json()[\'data\'][\'id\']\n\1{created_ids_var}.append(\2)'
    content = re.sub(create_pattern, replacement, content)
    
    # Добавляем сохранение ID в тесты создания
    create_success_pattern = r'(\s+)(json_data\s*=\s*response\.json\(\)\s*\n\s+assert \'data\' in json_data[^\n]*\n\s+)(\w+_data\s*=\s*json_data\[\'data\'\]\s*\n\s+assert \'id\' in \w+_data[^\n]*\s*\n\s+)(print\([^)]*\))'
    replacement = r'\1\2\3\1# Сохраняем ID для последующего удаления\n\1{created_ids_var}.append(\w+_data[\'id\'])\n\1\n\1\4'
    content = re.sub(create_success_pattern, replacement, content)
    
    # Записываем обновленный контент
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Добавлена очистка в файл: {file_path}")
    return True

def main():
    """Основная функция"""
    
    # Пути к тестовым файлам
    test_dirs = [
        'tests/tests_microservices/tests_incidents/test_keywords',
        'tests/tests_microservices/tests_incidents/test_response_scenarios',
        'tests/tests_microservices/tests_incidents/test_daily_worksheets',
        'tests/tests_microservices/tests_incidents/test_categories',
        'tests/tests_microservices/tests_incidents/test_events'
    ]
    
    updated_files = []
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            for file_path in Path(test_dir).glob('test_*.py'):
                if add_cleanup_to_test_file(file_path):
                    updated_files.append(file_path)
    
    print(f"\nОбновлено файлов: {len(updated_files)}")
    for file_path in updated_files:
        print(f"  - {file_path}")

if __name__ == '__main__':
    main() 