#!/usr/bin/env python3
"""
API клиент для раздела Метрополитен
"""

import requests
import os
from datetime import datetime


class MetroAPIClient:
    """API клиент для работы с разделом Метрополитен"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/transport-metro/api"
        self.report_base_url = "http://91.227.17.139/services/report/api"
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
        Делает POST запрос к /vestibule и проверяет статус ответа
        Returns:
            dict: {"valid": bool, "status_code": int, "message": str}
        """
        try:
            response = requests.post(
                f"{self.base_url}/vestibule",
                json={"page": 1, "limit": 1},
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
    
    # === Вестибюли ===
    
    def get_vestibules_on_page(self, page=1, limit=500):
        """
        Получить список вестибюлей на странице
        """
        data = {"page": page, "limit": limit}
        return requests.post(f"{self.base_url}/vestibule", json=data, headers=self.headers, verify=False)
    
    def get_vestibule_traffic_thresholds_list(self):
        """
        Получить список вестибюлей (пороги пассажиропотока)
        """
        data = {}
        return requests.post(f"{self.base_url}/vestibule-traffic-threshold/list", json=data, headers=self.headers, verify=False)
    
    def update_vestibule_traffic_thresholds(self, thresholds_data):
        """
        Редактирование порогов пассажиропотока
        
        Args:
            thresholds_data: list - список объектов с данными порогов
                Пример: [
                    {
                        "id": 21,
                        "vestibule_id": 1,
                        "time_start": "01:00:00",
                        "time_end": "02:00:00",
                        "count": 100,
                        "updated_at": "2025-08-15T13:25:56+00:00",
                        "updated_by": None
                    }
                ]
        """
        return requests.put(f"{self.base_url}/vestibule-traffic-threshold", json=thresholds_data, headers=self.headers, verify=False)
    
    # === Отчеты ===
    
    def get_vestibule_traffic_report(self, start_date, end_date):
        """
        Получить отчет о пассажирах
        
        Args:
            start_date: str - дата начала в формате "2025-10-25T00:00:00+03:00"
            end_date: str - дата окончания в формате "2025-10-25T23:59:59+03:00"
        """
        data = {
            "start_date": start_date,
            "end_date": end_date
        }
        return requests.post(f"{self.base_url}/vestibule/traffic", json=data, headers=self.headers, verify=False)
    
    def generate_passenger_report(self, start_date, end_date, formats=None):
        """
        Формирование отчета о пассажирах
        
        Args:
            start_date: str - дата начала в формате "2025-10-25"
            end_date: str - дата окончания в формате "2025-10-25"
            formats: list - форматы отчета, например ["HTML", "CSV", "XLSX"]
        """
        if formats is None:
            formats = ["HTML", "CSV", "XLSX"]
        
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "formats": formats
        }
        return requests.post(f"{self.report_base_url}/v2/report/request/31", json=data, headers=self.headers, verify=False)

