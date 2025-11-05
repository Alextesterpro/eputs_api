#!/usr/bin/env python3
"""
Общие настройки для всех тестов
"""

import pytest
import sys
import os

# Добавляем корневую папку в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_clients import (
    IncidentsAPIClient,
    DTPAPIClient,
    MetroAPIClient,
    ParkingAPIClient,
    DigitalTwinAPIClient,
    ExternalTransportAPIClient,
    WaterTransportAPIClient,
    PassengerTransportAPIClient,
    DataBusAPIClient
)


@pytest.fixture(scope="module")
def incidents_client():
    """Фикстура для предоставления API клиента инцидентов"""
    return IncidentsAPIClient()


@pytest.fixture(scope="module")
def dtp_client():
    """Фикстура для предоставления API клиента ДТП"""
    return DTPAPIClient()


@pytest.fixture(scope="module")
def metro_client():
    """Фикстура для предоставления API клиента Метрополитен"""
    return MetroAPIClient()


@pytest.fixture(scope="module")
def parking_client():
    """Фикстура для предоставления API клиента Парковочное пространство"""
    return ParkingAPIClient()


@pytest.fixture(scope="module")
def digital_twin_client():
    """Фикстура для предоставления API клиента Цифровой двойник"""
    return DigitalTwinAPIClient()


@pytest.fixture(scope="module")
def external_transport_client():
    """Фикстура для предоставления API клиента Внешний транспорт"""
    return ExternalTransportAPIClient()


@pytest.fixture(scope="module")
def water_transport_client():
    """Фикстура для предоставления API клиента Водный транспорт"""
    return WaterTransportAPIClient()


@pytest.fixture(scope="module")
def passenger_transport_client():
    """Фикстура для предоставления API клиента Пассажирский транспорт"""
    return PassengerTransportAPIClient()


@pytest.fixture(scope="module")
def data_bus_client():
    """Фикстура для предоставления API клиента Data Bus (Общая шина)"""
    return DataBusAPIClient()

