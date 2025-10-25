#!/usr/bin/env python3
"""
Простой API клиент для инцидентов
"""

import requests
import json
import os


class SimpleIncidentAPI:
    """Простой API для работы с инцидентами"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/react/api"
        self.token = self._get_token()
    
    def _get_token(self):
        """Получить токен из файла"""
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
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "project": "98_spb",
            "service": "eputs"
        }
    
    def list_incidents(self, page=1, limit=10):
        """Получить список инцидентов"""
        data = {"page": page, "limit": limit, "is_simple": True}
        response = requests.post(
            f"{self.base_url}/incident/list", 
            json=data, 
            headers=self._get_headers(), 
            verify=False
        )
        return response
    
    def get_incident(self, incident_id):
        """Получить один инцидент"""
        response = requests.get(
            f"{self.base_url}/incident/{incident_id}", 
            headers=self._get_headers(), 
            verify=False
        )
        return response
    
    def search_incidents(self, page=1, limit=10):
        """Поиск инцидентов"""
        data = {"page": page, "limit": limit}
        response = requests.post(
            f"{self.base_url}/incident/search", 
            json=data, 
            headers=self._get_headers(), 
            verify=False
        )
        return response
    
    def create_incident(self, name, description):
        """Создать инцидент"""
        data = {"name": name, "description": description}
        response = requests.post(
            f"{self.base_url}/incident", 
            json=data, 
            headers=self._get_headers(), 
            verify=False
        )
        return response
