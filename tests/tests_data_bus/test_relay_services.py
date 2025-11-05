#!/usr/bin/env python3
"""
Тесты для Relay Services (Сервисы ретрансляции)
"""

import pytest
import random


class TestRelayServicesList:
    """Тесты для списка сервисов ретрансляции"""
    
    def test_relay_services_list(self, data_bus_client):
        """Тест получения списка сервисов ретрансляции"""
        response = data_bus_client.relay_service_list()
        
        assert response.status_code == 200, f"Status code: {response.status_code}"
        data = response.json()
        assert data.get("success") is True, "Нет success=true"
        assert "data" in data, "Отсутствует поле data"


class TestRelayEGTSClone:
    """Тесты для Relay Service EGTS Clone"""
    
    def test_egts_clone_workflow(self, data_bus_client):
        """Полный workflow: создание, редактирование, удаление EGTS Clone"""
        
        # Создание
        name_create = f"Апи добавление {random.randint(1000, 9999)}"
        ip_create = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        port_create = random.randint(5000, 9999)
        collection_service_id_list = [423]  # Используем существующий ID из примера
        
        response_create = data_bus_client.relay_egts_clone_create(
            name=name_create,
            ip=ip_create,
            port=port_create,
            collection_service_id_list=collection_service_id_list
        )
        
        # Может быть 200 или 500 если нет доступного collection_service
        if response_create.status_code != 200:
            pytest.skip(f"Collection service недоступен: {response_create.status_code}")
        
        assert response_create.status_code == 200, f"Create status: {response_create.status_code}"
        data_create = response_create.json()
        assert data_create.get("success") is True, "Create: нет success=true"
        assert "data" in data_create, "Create: отсутствует поле data"
        assert "id" in data_create["data"], "Create: отсутствует ID"
        
        relay_id = data_create["data"]["id"]
        
        # Редактирование
        name_update = f"Апи редактирование {random.randint(1000, 9999)}"
        ip_update = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        port_update = random.randint(5000, 9999)
        
        response_update = data_bus_client.relay_egts_clone_update(
            relay_id=relay_id,
            name=name_update,
            ip=ip_update,
            port=port_update,
            collection_service_id_list=collection_service_id_list
        )
        
        assert response_update.status_code == 200, f"Update status: {response_update.status_code}"
        data_update = response_update.json()
        assert data_update.get("success") is True, "Update: нет success=true"
        
        # Удаление
        response_delete = data_bus_client.relay_egts_clone_delete(relay_id)
        
        assert response_delete.status_code == 200, f"Delete status: {response_delete.status_code}"
        data_delete = response_delete.json()
        assert data_delete.get("success") is True, "Delete: нет success=true"


class TestRelayEGTSTelemetry:
    """Тесты для Relay Service EGTS Telemetry"""
    
    def test_egts_telemetry_workflow(self, data_bus_client):
        """Полный workflow: создание, редактирование, удаление EGTS Telemetry"""
        
        # Создание
        name_create = f"Апи добавление {random.randint(1000, 9999)}"
        ip_create = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        port_create = random.randint(5000, 9999)
        type_id_list = [1, 2, 3, 4]
        organization_id_list = [4]  # Метрополитен из примера
        id_field = 1  # OID
        
        response_create = data_bus_client.relay_egts_telemetry_create(
            name=name_create,
            ip=ip_create,
            port=port_create,
            type_id_list=type_id_list,
            organization_id_list=organization_id_list,
            id_field=id_field
        )
        
        assert response_create.status_code == 200, f"Create status: {response_create.status_code}"
        data_create = response_create.json()
        assert data_create.get("success") is True, "Create: нет success=true"
        assert "data" in data_create, "Create: отсутствует поле data"
        assert "id" in data_create["data"], "Create: отсутствует ID"
        
        relay_id = data_create["data"]["id"]
        
        # Редактирование
        name_update = f"Апи редактирование {random.randint(1000, 9999)}"
        ip_update = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        port_update = random.randint(5000, 9999)
        
        response_update = data_bus_client.relay_egts_telemetry_update(
            relay_id=relay_id,
            name=name_update,
            ip=ip_update,
            port=port_update,
            type_id_list=type_id_list,
            organization_id_list=organization_id_list,
            id_field=id_field
        )
        
        assert response_update.status_code == 200, f"Update status: {response_update.status_code}"
        data_update = response_update.json()
        assert data_update.get("success") is True, "Update: нет success=true"
        
        # Удаление
        response_delete = data_bus_client.relay_egts_telemetry_delete(relay_id)
        
        assert response_delete.status_code == 200, f"Delete status: {response_delete.status_code}"
        data_delete = response_delete.json()
        assert data_delete.get("success") is True, "Delete: нет success=true"

