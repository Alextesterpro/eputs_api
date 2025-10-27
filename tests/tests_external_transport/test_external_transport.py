#!/usr/bin/env python3
"""
Тесты для раздела Внешний транспорт
"""

import pytest


class TestStations:
    """Тесты для станций"""
    
    def test_stations_list(self, external_transport_client):
        """Тест получения списка станций"""
        result = external_transport_client.get_stations_list(page=1, limit=25)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print(f"Stations list: найдено {len(data.get('data', []))} станций")
    
    def test_transport_types(self, external_transport_client):
        """Тест получения списка видов транспорта"""
        result = external_transport_client.get_transport_types()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print(f"Transport types: найдено {len(data.get('data', []))} видов транспорта")
    
    def test_statuses(self, external_transport_client):
        """Тест получения списка статусов"""
        result = external_transport_client.get_statuses()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print(f"Statuses: найдено {len(data.get('data', []))} статусов")
    
    def test_relocation_states(self, external_transport_client):
        """Тест получения списка состояний перемещений бортов"""
        result = external_transport_client.get_relocation_states()
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print(f"Relocation states: найдено {len(data.get('data', []))} состояний")


class TestReports:
    """Тесты для отчетов"""
    
    def test_flight_schedules(self, external_transport_client):
        """Тест отчета о прибытии авиарейсов ВВСС"""
        result = external_transport_client.get_flight_schedules(
            start_date="2025-10-24",
            end_date="2025-10-25",
            id_list=[518],
            page=1,
            limit=25
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Flight schedules report работает")
    
    def test_generate_flight_report_xlsx(self, external_transport_client):
        """Тест формирования отчета о прибытии в формате XLSX"""
        result = external_transport_client.generate_flight_report(
            start_date="2025-10-24",
            end_date="2025-10-25",
            id_list=[518],
            formats=["XLSX"],
            report_id=38
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Flight report XLSX generation работает")
    
    def test_generate_flight_report_ods(self, external_transport_client):
        """Тест формирования отчета о прибытии в формате ODS"""
        result = external_transport_client.generate_flight_report(
            start_date="2025-10-24",
            end_date="2025-10-25",
            id_list=[518],
            formats=["ODS"],
            report_id=38
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Flight report ODS generation работает")
    
    def test_passenger_count_report(self, external_transport_client):
        """Тест отчета по проходам ЖД"""
        result = external_transport_client.get_passenger_count_report(
            date="2025-10-25T00:00:00+03:00",
            page=1,
            limit=25
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Passenger count report работает")

