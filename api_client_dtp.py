#!/usr/bin/env python3
"""
API клиент для раздела ДТП
"""

import requests
import os


class DTPAPIClient:
    """API клиент для ДТП"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services"
        self.token = self._get_token()
        self.headers = self._get_headers()
    
    def _get_token(self):
        """Получить токен"""
        token_file = ".env"
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                for line in f:
                    if line.startswith('EPUTS_TOKEN='):
                        return line.split('=', 1)[1].strip()
        return os.getenv("EPUTS_TOKEN", "NOT_SET")
    
    def _get_headers(self):
        """Получить заголовки"""
        if not self.token:
            raise ValueError("Токен не найден! Запустите simple_login.py")
        
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "project": "98_spb",
            "service": "dtp"
        }
    
    def check_token(self):
        """
        Проверить валидность токена
        Делает GET запрос к /dtp/api/dtp/types и проверяет статус ответа
        Returns:
            dict: {"valid": bool, "status_code": int, "message": str}
        """
        try:
            response = requests.get(
                f"{self.base_url}/dtp/api/dtp/types",
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
    
    # === DTP TYPES ===
    def get_dtp_types(self, page=1, limit=25):
        """Получить список типов ДТП"""
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.base_url}/dtp/api/dtp/types", params=params, headers=self.headers, verify=False)
    
    # === POPULATION ===
    def get_population_list(self, page=1, limit=25):
        """Получить список населения"""
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.base_url}/dtp/api/population", params=params, headers=self.headers, verify=False)
    
    def create_population(self, year, count):
        """Создать запись населения"""
        data = {"year": year, "count": count}
        return requests.post(f"{self.base_url}/dtp/api/population", json=data, headers=self.headers, verify=False)
    
    def update_population(self, population_id, year, count):
        """Обновить запись населения"""
        data = {"year": year, "count": count}
        return requests.put(f"{self.base_url}/dtp/api/population/{population_id}", json=data, headers=self.headers, verify=False)
    
    def delete_population(self, population_id):
        """Удалить запись населения"""
        return requests.delete(f"{self.base_url}/dtp/api/population/{population_id}", headers=self.headers, verify=False)
    
    # === DTP CONCENTRATION AREA (МКДТП) ===
    def get_dtp_concentration_areas(self, page=1, limit=25, start_date=None, end_date=None, with_dtp_list=1):
        """Получить список МКДТП"""
        params = {"page": page, "limit": limit, "with_dtp_list": with_dtp_list}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return requests.get(f"{self.base_url}/dtp/api/dtp-concentration-area", params=params, headers=self.headers, verify=False)
    
    def create_dtp_concentration_area(self, name, dtp_type, status, address, lat, lon, description, dtp_ids):
        """Создать МКДТП"""
        from datetime import datetime
        
        data = {
            "name": name,
            "type": dtp_type,
            "status": status,
            "address": address,
            "address_text": f"{address.get('city_name', '')}, {address.get('street', '')}, {address.get('house', '')}",
            "lat": lat,
            "lon": lon,
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "confirmed_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "transport_incident_id": None,
            "description": description,
            "dtp_ids": dtp_ids,
            "dtp_list": [],
            "polygon": None
        }
        return requests.post(f"{self.base_url}/dtp/api/dtp-concentration-area", json=data, headers=self.headers, verify=False)
    
    def update_dtp_concentration_area(self, mkdtp_id, **fields):
        """Обновить МКДТП"""
        return requests.put(f"{self.base_url}/dtp/api/dtp-concentration-area/{mkdtp_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_dtp_concentration_area(self, mkdtp_id):
        """Удалить МКДТП"""
        return requests.delete(f"{self.base_url}/dtp/api/dtp-concentration-area/{mkdtp_id}", headers=self.headers, verify=False)
    
    # === DTP (ДТП) ===
    def get_dtp_list(self, page=1, limit=25, start_date=None, end_date=None):
        """Получить список ДТП"""
        data = {"page": page, "limit": limit}
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        return requests.post(f"{self.base_url}/dtp/api/v2/dtp/list", json=data, headers=self.headers, verify=False)
    
    def create_dtp(self, status, dtp_type, dtp_at, address, lat, lon, description, geometry):
        """Создать ДТП"""
        data = {
            "status": status,
            "dtp_type": dtp_type,
            "manual_edit": True,
            "dtp_at": dtp_at,
            "address": address,
            "lat": lat,
            "lon": lon,
            "km": None,
            "m": None,
            "description": description,
            "ti_id": None,
            "ti_name": None,
            "count_members": 1,
            "count_ts": 1,
            "geometry": geometry,
            "address_text": f"{address.get('city_name', '')}, {address.get('street', '')}, {address.get('house', '')}"
        }
        return requests.post(f"{self.base_url}/dtp/api/dtp", json=data, headers=self.headers, verify=False)
    
    def update_dtp(self, dtp_id, **fields):
        """Обновить ДТП"""
        return requests.put(f"{self.base_url}/dtp/api/dtp/{dtp_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_dtp(self, dtp_id):
        """Удалить ДТП"""
        return requests.delete(f"{self.base_url}/dtp/api/dtp/{dtp_id}", headers=self.headers, verify=False)
    
    # === DTP REPORTS ===
    def get_dtp_report_by_percent(self, start_date, end_date, with_wounded=0, with_dead=0, report=None):
        """Получить отчет по типам ДТП"""
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "with_wounded": with_wounded,
            "with_dead": with_dead
        }
        if report:
            params["report"] = report
        return requests.get(f"{self.base_url}/dtp/api/report/by-percent", params=params, headers=self.headers, verify=False)
    
    def get_dtp_heatmap(self, polygon, type_load, start_date, end_date, with_wounded, with_dead, dtp_type):
        """Получить тепловую карту ДТП"""
        data = {
            "polygon": polygon,
            "type_load": type_load,
            "start_date": start_date,
            "end_date": end_date,
            "with_wounded": with_wounded,
            "with_dead": with_dead,
            "dtp_type": dtp_type
        }
        return requests.post(f"{self.base_url}/dtp/api/dtp/polygon", json=data, headers=self.headers, verify=False)
    
    def get_dtp_by_time(self, start_date, end_date, start_time, end_time):
        """Получить отчет ДТП по времени"""
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "start_time": start_time,
            "end_time": end_time
        }
        return requests.post(f"{self.base_url}/dtp/api/dtp/by-time", json=data, headers=self.headers, verify=False)
    
    def get_dtp_count_by_periods(self, dates, selected_types=None, types=None):
        """Получить отчет по сравнению периодов"""
        data = {
            "dates": dates,
            "selectedTypes": selected_types or [],
            "types": types or []
        }
        return requests.post(f"{self.base_url}/dtp/api/v2/dtp/count-by-periods", json=data, headers=self.headers, verify=False)
