#!/usr/bin/env python3
"""
Простой сервисный слой
"""

from api_client import SimpleAPIClient


class SimpleIncidentService:
    """Простой сервис для работы с инцидентами"""
    
    def __init__(self):
        self.client = SimpleAPIClient()
    
    def get_all_incidents(self, page=1, limit=10):
        """Получить все инциденты"""
        response = self.client.get_incidents_list(page=page, limit=limit)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения списка: {response.status_code}")
    
    def get_incident_by_id(self, incident_id):
        """Получить инцидент по ID"""
        response = self.client.get_incident_by_id(incident_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения инцидента: {response.status_code}")
    
    def search_incidents(self, page=1, limit=10):
        """Поиск инцидентов"""
        response = self.client.search_incidents(page=page, limit=limit)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка поиска: {response.status_code}")
    
    def create_incident(self, name, description):
        """Создать новый инцидент"""
        response = self.client.create_incident(name, description)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка создания: {response.status_code}")
    
    def update_incident(self, incident_id, **fields):
        """Обновить инцидент"""
        response = self.client.update_incident(incident_id, **fields)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка обновления: {response.status_code}")
    
    def delete_incident(self, incident_id):
        """Удалить инцидент"""
        response = self.client.delete_incident(incident_id)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Ошибка удаления: {response.status_code}")
    
    def is_api_available(self):
        """Проверить доступность API"""
        try:
            response = self.client.get_incidents_list(page=1, limit=1)
            return response.status_code in [200, 401]
        except:
            return False
