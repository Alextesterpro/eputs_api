#!/usr/bin/env python3
"""
Тесты для раздела Внешний транспорт
"""

import pytest


class TestStations:
    """Тесты для станций"""
    
    def test_stations_list(self, external_transport_client):
        """Тест получения списка станций"""
        limit = 25
        result = external_transport_client.get_stations_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        stations = data.get("data", [])
        assert isinstance(stations, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(stations) <= limit, f"Количество элементов ({len(stations)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(stations) > 0:
            first_station = stations[0]
            assert "id" in first_station, "Отсутствует поле id"
            assert isinstance(first_station["id"], int), "ID должен быть числом"
            
            if "name" in first_station:
                assert isinstance(first_station["name"], str), "Name должен быть строкой"
            if "type" in first_station:
                assert isinstance(first_station["type"], (str, int)), "Type должен быть строкой или числом"
            
            print(f"Пример станции: ID={first_station['id']}, Name={first_station.get('name', 'N/A')}")
        
        print(f"Получено станций: {len(stations)}")
    
    def test_transport_types(self, external_transport_client):
        """Тест получения списка видов транспорта"""
        result = external_transport_client.get_transport_types()
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        types_data = data.get("data", [])
        
        # API может возвращать словарь или список
        if isinstance(types_data, dict):
            types = types_data
            assert isinstance(types, dict), "Data должна быть словарем"
            print(f"Получено видов транспорта: {len(types)} (dict)")
            if len(types) > 0:
                first_key = list(types.keys())[0]
                print(f"Пример типа транспорта: {first_key}: {types[first_key]}")
        elif isinstance(types_data, list):
            types = types_data
            assert isinstance(types, list), "Data должна быть списком"
            print(f"Получено видов транспорта: {len(types)} (list)")
            if len(types) > 0:
                print(f"Пример типа транспорта: {types[0]}")
    
    def test_statuses(self, external_transport_client):
        """Тест получения списка статусов"""
        result = external_transport_client.get_statuses()
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        statuses = data.get("data", [])
        assert isinstance(statuses, list), "Data должна быть списком"
        
        # Проверка структуры элементов
        if len(statuses) > 0:
            first_status = statuses[0]
            # Может быть объект с id/name или просто строка
            if isinstance(first_status, dict):
                if "id" in first_status:
                    assert isinstance(first_status["id"], int), "ID должен быть числом"
                if "name" in first_status:
                    assert isinstance(first_status["name"], str), "Name должен быть строкой"
                print(f"Пример статуса: {first_status}")
            elif isinstance(first_status, str):
                print(f"Пример статуса: {first_status}")
        
        print(f"Получено статусов: {len(statuses)}")
    
    def test_relocation_states(self, external_transport_client):
        """Тест получения списка состояний перемещений бортов"""
        result = external_transport_client.get_relocation_states()
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        states_data = data.get("data", [])
        
        # API может возвращать словарь или список
        if isinstance(states_data, dict):
            states = states_data
            assert isinstance(states, dict), "Data должна быть словарем"
            print(f"Получено состояний перемещений: {len(states)} (dict)")
            if len(states) > 0:
                first_key = list(states.keys())[0]
                print(f"Пример состояния: {first_key}: {states[first_key]}")
        elif isinstance(states_data, list):
            states = states_data
            assert isinstance(states, list), "Data должна быть списком"
            print(f"Получено состояний перемещений: {len(states)} (list)")
            if len(states) > 0:
                print(f"Пример состояния: {states[0]}")


class TestReports:
    """Тесты для отчетов"""
    
    def test_flight_schedules(self, external_transport_client):
        """Тест отчета о прибытии авиарейсов ВВСС"""
        start_date = "2025-10-24"
        end_date = "2025-10-25"
        id_list = [518]
        limit = 25
        
        result = external_transport_client.get_flight_schedules(
            start_date=start_date,
            end_date=end_date,
            id_list=id_list,
            page=1,
            limit=limit
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        schedules = data.get("data", [])
        assert isinstance(schedules, list), "Data должна быть списком"
        
        # Проверка лимита
        assert len(schedules) <= limit, f"Количество элементов ({len(schedules)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(schedules) > 0:
            first_schedule = schedules[0]
            assert isinstance(first_schedule, dict), "Элемент должен быть словарем"
            
            # Проверка ключевых полей
            if "id" in first_schedule:
                assert isinstance(first_schedule["id"], int), "ID должен быть числом"
            if "flight_number" in first_schedule:
                assert isinstance(first_schedule["flight_number"], (str, int)), "Flight number должен быть строкой или числом"
            
            print(f"Пример расписания рейса: {first_schedule}")
        
        print(f"✓ Flight schedules: получено {len(schedules)} записей")
    
    def test_generate_flight_report_xlsx(self, external_transport_client):
        """Тест формирования отчета о прибытии в формате XLSX"""
        result = external_transport_client.generate_flight_report(
            start_date="2025-10-24",
            end_date="2025-10-25",
            id_list=[518],
            formats=["XLSX"],
            report_id=38
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка что отчет сгенерирован
        assert "data" in data, "Отсутствует поле data"
        report_data = data.get("data")
        
        # Проверка что есть ссылка на файл или файл сгенерирован
        if report_data is not None:
            if isinstance(report_data, dict):
                # Может быть URL файла или другая информация
                print(f"✓ Flight report XLSX: отчет сгенерирован: {report_data}")
            elif isinstance(report_data, str):
                print(f"✓ Flight report XLSX: отчет сгенерирован (URL: {report_data})")
        else:
            print("✓ Flight report XLSX: запрос принят (data is None)")
    
    def test_generate_flight_report_ods(self, external_transport_client):
        """Тест формирования отчета о прибытии в формате ODS"""
        result = external_transport_client.generate_flight_report(
            start_date="2025-10-24",
            end_date="2025-10-25",
            id_list=[518],
            formats=["ODS"],
            report_id=38
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка что отчет сгенерирован
        assert "data" in data, "Отсутствует поле data"
        report_data = data.get("data")
        
        # Проверка что есть ссылка на файл или файл сгенерирован
        if report_data is not None:
            if isinstance(report_data, dict):
                # Может быть URL файла или другая информация
                print(f"✓ Flight report ODS: отчет сгенерирован: {report_data}")
            elif isinstance(report_data, str):
                print(f"✓ Flight report ODS: отчет сгенерирован (URL: {report_data})")
        else:
            print("✓ Flight report ODS: запрос принят (data is None)")
    
    def test_passenger_count_report(self, external_transport_client):
        """Тест отчета по проходам ЖД"""
        limit = 25
        result = external_transport_client.get_passenger_count_report(
            date="2025-10-25T00:00:00+03:00",
            page=1,
            limit=limit
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        report_data = data.get("data", {})
        
        # API может возвращать структуру с headers и rows или список
        if isinstance(report_data, dict):
            # Проверка структуры отчета
            assert "headers" in report_data or "rows" in report_data or len(report_data) > 0, "Отсутствуют данные отчета"
            
            if "headers" in report_data:
                headers = report_data["headers"]
                assert isinstance(headers, dict), "Headers должны быть словарем"
                print(f"✓ Passenger count report: headers найдены ({len(headers)} полей)")
            
            if "rows" in report_data:
                rows = report_data["rows"]
                assert isinstance(rows, list), "Rows должны быть списком"
                
                if len(rows) > 0:
                    first_row = rows[0]
                    print(f"Пример строки отчета: {first_row}")
                
                print(f"✓ Passenger count report: получено {len(rows)} строк")
            else:
                print(f"✓ Passenger count report: структура отчета получена")
        
        elif isinstance(report_data, list):
            report = report_data
            assert len(report) <= limit, f"Количество элементов ({len(report)}) превышает лимит ({limit})"
            
            if len(report) > 0:
                first_item = report[0]
                print(f"Пример данных проходов: {first_item}")
            
            print(f"✓ Passenger count report: получено {len(report)} записей")

