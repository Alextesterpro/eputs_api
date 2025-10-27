#!/usr/bin/env python3
"""
API клиент для раздела Внешний транспорт
"""

import requests
import os


class ExternalTransportAPIClient:
    """API клиент для работы с внешним транспортом"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/transport-external/api"
        self.report_url = "http://91.227.17.139/services/report/api"
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
        """Проверить валидность токена"""
        try:
            response = requests.get(
                f"{self.base_url}/station",
                params={"page": 1, "limit": 1},
                headers=self.headers,
                verify=False,
                timeout=10
            )
            
            if response.status_code == 401:
                return {"valid": False, "status_code": 401, "message": "Токен недействителен или протух (401 Unauthorized)"}
            elif response.status_code == 403:
                return {"valid": False, "status_code": 403, "message": "Нет доступа (403 Forbidden)"}
            elif response.status_code in [200, 201]:
                return {"valid": True, "status_code": response.status_code, "message": "Токен валиден"}
            else:
                return {"valid": False, "status_code": response.status_code, "message": f"Неожиданный статус код: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"valid": False, "status_code": 0, "message": f"Ошибка соединения: {str(e)}"}
    
    # === Станции ===
    
    def get_stations_list(self, page=1, limit=25):
        """Получить список станций"""
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.base_url}/station", params=params, headers=self.headers, verify=False)
    
    def get_transport_types(self):
        """Получить список видов транспорта"""
        return requests.get(f"{self.base_url}/station/transport_types", headers=self.headers, verify=False)
    
    def get_statuses(self):
        """Получить список статусов"""
        return requests.get(f"{self.base_url}/station/statuses", headers=self.headers, verify=False)
    
    def get_relocation_states(self):
        """Получить список состояний перемещений бортов"""
        return requests.get(f"{self.base_url}/v2/station/relocation-state", headers=self.headers, verify=False)
    
    # === Отчеты ===
    
    def get_flight_schedules(self, start_date, end_date, id_list, page=1, limit=25):
        """
        Получить отчет о прибытии авиарейсов ВВСС
        
        Args:
            start_date: str - дата начала (формат: YYYY-MM-DD)
            end_date: str - дата окончания (формат: YYYY-MM-DD)
            id_list: list - список ID станций
            page: int - номер страницы
            limit: int - количество записей на странице
        """
        data = {
            "page": page,
            "limit": limit,
            "start_date": start_date,
            "end_date": end_date,
            "id_list": id_list
        }
        return requests.post(f"{self.base_url}/v2/station/schedules", json=data, headers=self.headers, verify=False)
    
    def generate_flight_report(self, start_date, end_date, id_list, formats, report_id=38):
        """
        Сформировать отчет о прибытии авиарейсов
        
        Args:
            start_date: str - дата начала (формат: YYYY-MM-DD)
            end_date: str - дата окончания (формат: YYYY-MM-DD)
            id_list: list - список ID станций
            formats: list - форматы отчета (например, ["XLSX"], ["ODS"])
            report_id: int - ID отчета (по умолчанию 38)
        """
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "id_list": id_list,
            "formats": formats
        }
        return requests.post(f"{self.report_url}/v2/report/request/{report_id}", json=data, headers=self.headers, verify=False)
    
    def get_passenger_count_report(self, date, page=1, limit=25):
        """
        Получить отчет по проходам ЖД
        
        Args:
            date: str - дата (формат: YYYY-MM-DDTHH:MM:SS+03:00)
            page: int - номер страницы
            limit: int - количество записей на странице
        """
        data = {
            "page": page,
            "limit": limit,
            "date": date
        }
        return requests.post(f"{self.base_url}/report/passenger-count", json=data, headers=self.headers, verify=False)

