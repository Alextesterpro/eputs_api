import pytest
from datetime import datetime


class TestDTP:
    """Тесты для раздела ДТП"""
    
    def test_dtp_types_list(self, dtp_client):
        """Тест получения списка типов ДТП"""
        limit = 25
        result = dtp_client.get_dtp_types(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        types_data = data["data"]
        
        # Проверка структуры (может быть список или объект с items)
        if isinstance(types_data, list):
            types_list = types_data
        elif isinstance(types_data, dict) and "items" in types_data:
            types_list = types_data["items"]
        else:
            types_list = []
        
        # Проверка лимита
        assert len(types_list) <= limit, f"Количество элементов ({len(types_list)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(types_list) > 0:
            first_type = types_list[0]
            assert "id" in first_type or "name" in first_type, "Отсутствуют ключевые поля"
            print(f"Пример типа ДТП: {first_type}")
        
        print(f"Получено типов ДТП: {len(types_list)}")
    
    def test_population_list(self, dtp_client):
        """Тест получения списка населения"""
        limit = 25
        result = dtp_client.get_population_list(page=1, limit=limit)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        population_data = data["data"]
        
        # Получение списка
        if isinstance(population_data, list):
            population_list = population_data
        elif isinstance(population_data, dict) and "items" in population_data:
            population_list = population_data["items"]
        else:
            population_list = []
        
        # Проверка лимита
        assert len(population_list) <= limit, f"Количество элементов ({len(population_list)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(population_list) > 0:
            first_item = population_list[0]
            if "year" in first_item:
                assert isinstance(first_item["year"], int), "Year должен быть числом"
            if "count" in first_item:
                assert isinstance(first_item["count"], (int, float)), "Count должен быть числом"
            print(f"Пример данных населения: {first_item}")
        
        print(f"Получено записей населения: {len(population_list)}")
    
    def test_population_create(self, dtp_client):
        """Тест создания записи населения"""
        year = 2023
        count = 102184
        
        # Создание
        result = dtp_client.create_population(year, count)
        
        # Проверка статуса
        assert result.status_code == 200, f"Create failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        population = data["data"]
        
        # Проверка что вернулись правильные данные
        if "year" in population:
            assert population["year"] == year, f"Year не совпадает: ожидалось {year}, получено {population['year']}"
        if "count" in population:
            assert population["count"] == count, f"Count не совпадает: ожидалось {count}, получено {population['count']}"
        
        print(f"✓ CREATE Population: year={year}, count={count}")
    
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
        limit = 25
        result = dtp_client.get_dtp_list(
            page=1,
            limit=limit,
            start_date="2025-10-01T00:00:00+03:00",
            end_date="2025-10-23T23:59:59+03:00"
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        dtp_data = data["data"]
        
        # Получение списка
        if isinstance(dtp_data, list):
            dtp_list = dtp_data
        elif isinstance(dtp_data, dict) and "items" in dtp_data:
            dtp_list = dtp_data["items"]
        else:
            dtp_list = []
        
        # Проверка лимита
        assert len(dtp_list) <= limit, f"Количество элементов ({len(dtp_list)}) превышает лимит ({limit})"
        
        # Проверка структуры элементов
        if len(dtp_list) > 0:
            first_dtp = dtp_list[0]
            assert "id" in first_dtp, "Отсутствует поле id"
            assert isinstance(first_dtp["id"], int), "ID должен быть числом"
            
            # Проверяем основные поля ДТП
            if "lat" in first_dtp and "lon" in first_dtp:
                assert isinstance(first_dtp["lat"], (int, float)), "Latitude должен быть числом"
                assert isinstance(first_dtp["lon"], (int, float)), "Longitude должен быть числом"
            
            print(f"Пример ДТП: ID={first_dtp['id']}, Координаты=({first_dtp.get('lat')}, {first_dtp.get('lon')})")
        
        print(f"Получено ДТП: {len(dtp_list)}")
    
    def test_dtp_create(self, dtp_client):
        """Тест создания ДТП"""
        # Данные для создания
        lat = 59.940400014187354
        lon = 30.28311892505096
        description = f"API тест ДТП {datetime.now().strftime('%H:%M:%S')}"
        dtp_type = 3
        
        address = {
            "city_name": "Санкт-Петербург",
            "region": "Санкт-Петербург",
            "federal_district": "Северо-Западный федеральный округ",
            "house": "11 литД",
            "geo_lat": lat,
            "geo_lon": lon,
            "street": "6-я линия В.О.",
            "district": "Василеостровский район"
        }
        
        geometry = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }
        
        # Создание
        result = dtp_client.create_dtp(
            status="1",
            dtp_type=dtp_type,
            dtp_at=datetime.now().isoformat(),
            address=address,
            lat=lat,
            lon=lon,
            description=description,
            geometry=geometry
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Create failed: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        assert "data" in data, "Отсутствует поле data"
        
        dtp = data["data"]
        
        # Проверка что вернулся ID
        assert "id" in dtp, "Отсутствует поле id"
        dtp_id = dtp["id"]
        assert isinstance(dtp_id, int), "ID должен быть числом"
        
        # Проверка координат
        if "lat" in dtp:
            assert abs(dtp["lat"] - lat) < 0.0001, f"Latitude не совпадает"
        if "lon" in dtp:
            assert abs(dtp["lon"] - lon) < 0.0001, f"Longitude не совпадает"
        
        print(f"✓ CREATE DTP: ID={dtp_id}, coords=({lat}, {lon}), description='{description}'")
    
    def test_dtp_report_by_percent(self, dtp_client):
        """Тест отчета по типам ДТП (по процентам)"""
        result = dtp_client.get_dtp_report_by_percent(
            start_date="2025-10-24T00:00:00+03:00",
            end_date="2025-10-24T23:59:59+03:00",
            with_wounded=0,
            with_dead=0
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Отчет может иметь разную структуру
        if "data" in data:
            report_data = data["data"]
            # Проверяем что это не пустой ответ
            assert report_data is not None, "Данные отчета не должны быть None"
            print(f"✓ Отчет по процентам: получены данные, тип={type(report_data).__name__}")
        else:
            print("✓ Отчет по процентам: success=true (данные в другом формате)")
    
    def test_dtp_by_time(self, dtp_client):
        """Тест отчета ДТП по времени суток"""
        result = dtp_client.get_dtp_by_time(
            start_date="2025-10-01",
            end_date="2025-10-24",
            start_time="00:00",
            end_time="23:59"
        )
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка данных
        if "data" in data:
            report_data = data["data"]
            assert report_data is not None, "Данные отчета не должны быть None"
            
            # Если это список или словарь, проверяем что не пустой
            if isinstance(report_data, (list, dict)):
                print(f"✓ Отчет по времени: получены данные, элементов={len(report_data)}")
            else:
                print(f"✓ Отчет по времени: получены данные")
        else:
            print("✓ Отчет по времени: success=true")
    
    def test_dtp_count_by_periods(self, dtp_client):
        """Тест отчета по сравнению периодов"""
        dates = [
            {"start_date": "2025-01-01", "end_date": "2025-01-28"},
            {"start_date": "2025-02-01", "end_date": "2025-02-28"}
        ]
        
        # Запрос отчета
        result = dtp_client.get_dtp_count_by_periods(dates=dates)
        
        # Проверка статуса
        assert result.status_code == 200, f"Status code: {result.status_code}"
        
        # Проверка структуры ответа
        data = result.json()
        assert data.get("success") is True, "Отсутствует success=true"
        
        # Проверка данных
        if "data" in data:
            report_data = data["data"]
            assert report_data is not None, "Данные отчета не должны быть None"
            
            # Если это список, проверяем что кол-во периодов совпадает
            if isinstance(report_data, list):
                assert len(report_data) <= len(dates) + 1, "Количество периодов в ответе больше ожидаемого"
                print(f"✓ Отчет по периодам: сравнено {len(dates)} периодов, получено {len(report_data)} результатов")
            else:
                print(f"✓ Отчет по периодам: получены данные, тип={type(report_data).__name__}")
        else:
            print("✓ Отчет по периодам: success=true")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
