#!/usr/bin/env python3
"""
API клиент для раздела Парковочное пространство
"""

import requests
import os
import random


class ParkingAPIClient:
    """API клиент для работы с парковками"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/parking/api"
        self.token = self._get_token()
        self.headers = self._get_headers()
    
    def _get_token(self):
        """Получить токен"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('EPUTS_TOKEN='):
                        return line.split('=', 1)[1].strip()
        except:
            pass
        return None
    
    def _get_headers(self):
        """Получить заголовки"""
        if not self.token:
            raise ValueError("Токен не найден! Запустите simple_login.py")
        
        return {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "project": "98_spb"
        }
    
    def check_token(self):
        """
        Проверить валидность токена
        Делает GET запрос к /parking и проверяет статус ответа
        Returns:
            dict: {"valid": bool, "status_code": int, "message": str}
        """
        try:
            response = requests.get(
                f"{self.base_url}/parking",
                params={"page": 1, "limit": 1},
                headers=self.headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 401:
                return {
                    "valid": False,
                    "status_code": 401,
                    "message": "Токен недействителен или протух (401 Unauthorized)"
                }
            elif response.status_code == 403:
                return {
                    "valid": False,
                    "status_code": 403,
                    "message": "Нет доступа (403 Forbidden)"
                }
            elif response.status_code in [200, 201]:
                return {
                    "valid": True,
                    "status_code": response.status_code,
                    "message": "Токен валиден"
                }
            else:
                return {
                    "valid": False,
                    "status_code": response.status_code,
                    "message": f"Неожиданный статус код: {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "valid": False,
                "status_code": 0,
                "message": f"Ошибка соединения: {str(e)}"
            }
    
    # === Парковки ===
    
    def get_parking_list(self, page=1, limit=25):
        """
        Получить список парковок
        """
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.base_url}/parking", params=params, headers=self.headers, verify=False)
    
    def create_parking(self, name, address, address_text, contacts, description, lat, lon, 
                      tariff_id=23, category_id=35, is_aggregating=True, is_blocked=True,
                      total="2", common="2", handicapped="2"):
        """
        Создать парковку
        
        Args:
            name: str - название парковки
            address: dict - объект адреса
            address_text: str - текстовое представление адреса
            contacts: str - контакты
            description: str - описание
            lat: float - широта
            lon: float - долгота
            tariff_id: int - ID тарифа (по умолчанию 23)
            category_id: int - ID категории (по умолчанию 35)
            is_aggregating: bool - агрегирование
            is_blocked: bool - заблокирована
            total: str - всего мест
            common: str - обычных мест
            handicapped: str - мест для инвалидов
        """
        data = {
            "name": name,
            "address": address,
            "address_text": address_text,
            "contacts": contacts,
            "description": description,
            "location": {
                "type": "Feature",
                "properties": {
                    "radius": 18.60439279274369
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                }
            },
            "tariff_id": tariff_id,
            "category_id": category_id,
            "photo": "http://91.227.17.139/services/storage//api/document/public/81379bcc85ca84c8e169060223a658e2",
            "is_aggregating": is_aggregating,
            "is_blocked": is_blocked,
            "total": total,
            "common": common,
            "handicapped": handicapped,
            "lat": lat,
            "lon": lon,
            "spaces": {
                "common": common,
                "total": total,
                "handicapped": handicapped
            }
        }
        return requests.post(f"{self.base_url}/parking", json=data, headers=self.headers, verify=False)
    
    def update_parking(self, parking_id, **fields):
        """
        Обновить парковку
        
        Args:
            parking_id: int - ID парковки
            **fields: дополнительные поля для обновления
        """
        return requests.put(f"{self.base_url}/parking/{parking_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_parking(self, parking_id):
        """
        Удалить парковку
        
        Args:
            parking_id: int - ID парковки
        """
        return requests.delete(f"{self.base_url}/parking/{parking_id}", headers=self.headers, verify=False)
    
    # === Вспомогательные методы ===
    
    @staticmethod
    def generate_test_address():
        """Генерировать тестовый адрес"""
        return {
            "city_name": "Санкт-Петербург",
            "region": "Санкт-Петербург",
            "federal_district": "Северо-Западный федеральный округ",
            "house": "4",
            "geo_lat": 59.94349,
            "geo_lon": 30.304595303107362,
            "street": "Биржевая площадь",
            "district": "Василеостровский район",
            "area_id": None,
            "city_id": 69,
            "postal_code": "199034",
            "area": "Санкт-Петербург",
            "settlement": None,
            "fias": None,
            "fias_code": None,
            "country_iso_code": "ru",
            "region_iso_code": None,
            "block": None,
            "flat": None,
            "postal_box": None,
            "kladr_id": None,
            "geoname_id": None,
            "okato": None,
            "oktmo": None,
            "tax_office": None,
            "tax_office_legal": None,
            "region_id": "",
            "city_type": None,
            "city_type_full": None
        }

