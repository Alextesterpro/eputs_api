#!/usr/bin/env python3
"""
Простой API клиент - без сложностей
"""

import requests
import os


class SimpleAPIClient:
    """Простой API клиент"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/react/api"
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
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "project": "98_spb",
            "service": "eputs"
        }
    
    def get_incidents_list(self, page=1, limit=10):
        """Получить список инцидентов"""
        data = {"page": page, "limit": limit, "is_simple": True}
        return requests.post(f"{self.base_url}/incident/list", json=data, headers=self.headers, verify=False)
    
    def get_incident_by_id(self, incident_id):
        """Получить инцидент по ID"""
        return requests.get(f"{self.base_url}/incident/{incident_id}", headers=self.headers, verify=False)
    
    def search_incidents(self, page=1, limit=10):
        """Поиск инцидентов"""
        data = {"page": page, "limit": limit}
        return requests.post(f"{self.base_url}/incident/search", json=data, headers=self.headers, verify=False)
    
    def create_incident(self, name, description):
        """Создать инцидент"""
        data = {"name": name, "description": description}
        return requests.post(f"{self.base_url}/incident", json=data, headers=self.headers, verify=False)
    
    def update_incident(self, incident_id, **fields):
        """Обновить инцидент"""
        return requests.put(f"{self.base_url}/incident/{incident_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_incident(self, incident_id):
        """Удалить инцидент"""
        return requests.delete(f"{self.base_url}/incident/{incident_id}", headers=self.headers, verify=False)
