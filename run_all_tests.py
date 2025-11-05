#!/usr/bin/env python3
"""
Скрипт для запуска тестов с различными опциями
"""

import pytest
import sys
import os
import argparse


MODULES = {
    'incidents': 'tests/tests_incidents/',
    'dtp': 'tests/tests_dtp/',
    'metro': 'tests/tests_metro/',
    'parking': 'tests/tests_parking/',
    'digital_twin': 'tests/tests_digital_twin/',
    'external_transport': 'tests/tests_external_transport/',
    'water_transport': 'tests/tests_water_transport/',
    'passenger_transport': 'tests/tests_passenger_transport/',
    'data_bus': 'tests/tests_data_bus/',
    'all': 'tests/'
}


def run_tests(module='all', verbose=True, parallel=False, allure=False, html=False, markers=None):
    """
    Запуск тестов с указанными параметрами
    
    Args:
        module: модуль для запуска (incidents, dtp, metro, parking, digital_twin, external_transport, water_transport, passenger_transport, all)
        verbose: подробный вывод
        parallel: параллельный запуск
        allure: генерация Allure отчета
        html: генерация HTML отчета
        markers: маркеры pytest (например, 'smoke', 'regression')
    """
    test_path = MODULES.get(module, 'tests/')
    
    print("=" * 60)
    print(f"Запуск тестов: {module.upper()}")
    print(f"Путь: {test_path}")
    print("=" * 60)
    
    # Базовые аргументы
    args = [test_path]
    
    # Verbose
    if verbose:
        args.extend(["-v", "--tb=short"])
    
    # Цвет
    args.append("--color=yes")
    
    # Параллельный запуск
    if parallel:
        args.extend(["-n", "auto"])
        print("Режим: параллельный запуск")
    
    # Allure отчет
    if allure:
        args.extend(["--alluredir", "allure-results"])
        print("Генерация: Allure отчет")
    
    # HTML отчет
    if html:
        args.extend(["--html", f"report_{module}.html", "--self-contained-html"])
        print("Генерация: HTML отчет")
    
    # Маркеры
    if markers:
        args.extend(["-m", markers])
        print(f"Маркеры: {markers}")
    
    print("=" * 60)
    
    # Запуск
    result = pytest.main(args)
    
    print("=" * 60)
    if result == 0:
        print("Все тесты прошли успешно!")
    else:
        print("Некоторые тесты не прошли")
    print("=" * 60)
    
    return result


def main():
    """Главная функция с парсингом аргументов"""
    parser = argparse.ArgumentParser(
        description='Запуск API тестов с различными опциями',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Запустить все тесты
  python3 run_all_tests.py

  # Запустить тесты конкретного модуля
  python3 run_all_tests.py --module dtp
  python3 run_all_tests.py --module water_transport

  # Запустить с Allure отчетом
  python3 run_all_tests.py --allure

  # Запустить с HTML отчетом
  python3 run_all_tests.py --html

  # Параллельный запуск
  python3 run_all_tests.py --parallel

  # Запустить только smoke тесты
  python3 run_all_tests.py --markers smoke

  # Комбинация опций
  python3 run_all_tests.py --module metro --allure --parallel

Доступные модули:
  - incidents         : Тесты инцидентов
  - dtp              : Тесты ДТП
  - metro            : Тесты метрополитен
  - parking          : Тесты парковок
  - digital_twin     : Тесты цифрового двойника
  - external_transport: Тесты внешнего транспорта
  - water_transport  : Тесты водного транспорта
  - all              : Все тесты (по умолчанию)
        """
    )
    
    parser.add_argument(
        '--module', '-m',
        type=str,
        default='all',
        choices=list(MODULES.keys()),
        help='Модуль для тестирования (по умолчанию: all)'
    )
    
    parser.add_argument(
        '--parallel', '-p',
        action='store_true',
        help='Параллельный запуск тестов (требует pytest-xdist)'
    )
    
    parser.add_argument(
        '--allure', '-a',
        action='store_true',
        help='Генерация Allure отчета'
    )
    
    parser.add_argument(
        '--html',
        action='store_true',
        help='Генерация HTML отчета'
    )
    
    parser.add_argument(
        '--markers',
        type=str,
        help='Фильтр по маркерам pytest (например: smoke, regression)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Минимальный вывод'
    )
    
    parser.add_argument(
        '--list-modules',
        action='store_true',
        help='Показать список доступных модулей'
    )
    
    args = parser.parse_args()
    
    # Список модулей
    if args.list_modules:
        print("\nДоступные модули для тестирования:")
        print("=" * 60)
        for name, path in MODULES.items():
            if name != 'all':
                print(f"  {name:20} -> {path}")
        print("=" * 60)
        return 0
    
    # Запуск тестов
    result = run_tests(
        module=args.module,
        verbose=not args.quiet,
        parallel=args.parallel,
        allure=args.allure,
        html=args.html,
        markers=args.markers
    )
    
    return result


if __name__ == "__main__":
    sys.exit(main())
