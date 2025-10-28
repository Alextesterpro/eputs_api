#!/usr/bin/env python3
"""
API клиенты для всех сервисов
"""

from .incidents import IncidentsAPIClient
from .dtp import DTPAPIClient
from .metro import MetroAPIClient
from .parking import ParkingAPIClient
from .digital_twin import DigitalTwinAPIClient
from .external_transport import ExternalTransportAPIClient
from .water_transport import WaterTransportAPIClient

__all__ = [
    'IncidentsAPIClient',
    'DTPAPIClient',
    'MetroAPIClient',
    'ParkingAPIClient',
    'DigitalTwinAPIClient',
    'ExternalTransportAPIClient',
    'WaterTransportAPIClient',
]

