import pytest
from datetime import datetime


class TestDTP:
    """Тесты для раздела ДТП"""
    
    def test_dtp_types_list(self, dtp_client):
        """Тест получения списка типов ДТП"""
        result = dtp_client.get_dtp_types(page=1, limit=25)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("DTP types list работает")
    
    def test_population_list(self, dtp_client):
        """Тест получения списка населения"""
        result = dtp_client.get_population_list(page=1, limit=25)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("Population list работает")
    
    def test_population_create(self, dtp_client):
        """Тест создания записи населения"""
        year = 2023
        count = 102184
        
        result = dtp_client.create_population(year, count)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Нет поля data"
        print("Population create работает")
    
    def test_dtp_concentration_areas_list(self, dtp_client):
        """Тест получения списка МКДТП"""
        result = dtp_client.get_dtp_concentration_areas(
            page=1, 
            limit=25,
            start_date="2025-01-01T00:00:00+03:00",
            end_date="2025-10-23T23:59:59+03:00"
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("DTP concentration areas list работает")
    
    def test_dtp_list(self, dtp_client):
        """Тест получения списка ДТП"""
        result = dtp_client.get_dtp_list(
            page=1,
            limit=25,
            start_date="2025-10-01T00:00:00+03:00",
            end_date="2025-10-23T23:59:59+03:00"
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("DTP list работает")
    
    def test_dtp_create(self, dtp_client):
        """Тест создания ДТП"""
        address = {
            "city_name": "Санкт-Петербург",
            "region": "Санкт-Петербург",
            "federal_district": "Северо-Западный федеральный округ",
            "house": "11 литД",
            "geo_lat": 59.940118600000005,
            "geo_lon": 30.283595855922243,
            "street": "6-я линия В.О.",
            "district": "Василеостровский район"
        }
        
        geometry = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [30.28311892505096, 59.940400014187354]
            }
        }
        
        result = dtp_client.create_dtp(
            status="1",
            dtp_type=3,
            dtp_at=datetime.now().isoformat(),
            address=address,
            lat=59.940400014187354,
            lon=30.28311892505096,
            description="API тест ДТП",
            geometry=geometry
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Нет поля data"
        print("DTP create работает")
    
    def test_dtp_report_by_percent(self, dtp_client):
        """Тест отчета по типам ДТП"""
        result = dtp_client.get_dtp_report_by_percent(
            start_date="2025-10-24T00:00:00+03:00",
            end_date="2025-10-24T23:59:59+03:00",
            with_wounded=0,
            with_dead=0
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("DTP report by percent работает")
    
    def test_dtp_by_time(self, dtp_client):
        """Тест отчета ДТП по времени"""
        result = dtp_client.get_dtp_by_time(
            start_date="2025-10-01",
            end_date="2025-10-24",
            start_time="00:00",
            end_time="23:59"
        )
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("DTP by time работает")
    
    def test_dtp_count_by_periods(self, dtp_client):
        """Тест отчета по сравнению периодов"""
        dates = [
            {"start_date": "2025-01-01", "end_date": "2025-01-28"},
            {"start_date": "2025-02-01", "end_date": "2025-02-28"}
        ]
        
        result = dtp_client.get_dtp_count_by_periods(dates=dates)
        assert result.status_code == 200, f"Status code: {result.status_code}"
        data = result.json()
        assert data.get("success") is True, "Нет success=true"
        print("DTP count by periods работает")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
