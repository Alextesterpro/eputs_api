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
    
    def create_incident(self, name, description, type_id=1, status_id=1, threat_level_id=1, category_id=1):
        """Создать инцидент с полными данными"""
        from datetime import datetime
        
        data = {
            "name": name,
            "description": description,
            "type_id": type_id,
            "status_id": status_id,
            "threat_level_id": threat_level_id,
            "category_id": category_id,
            "geometry": {
                "type": "Point",
                "coordinates": [30.3158, 59.9311]  # St. Petersburg coordinates
            },
            "registered_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "resolve_rules": 1
        }
        return requests.post(f"{self.base_url}/incident", json=data, headers=self.headers, verify=False)
    
    def update_incident(self, incident_id, **fields):
        """Обновить инцидент с полными данными"""
        from datetime import datetime
        
        # Если не переданы обязательные поля, используем значения по умолчанию
        data = {
            "name": fields.get("name", "Обновленный инцидент"),
            "description": fields.get("description", "Обновленное описание"),
            "type_id": fields.get("type_id", 1),
            "status_id": fields.get("status_id", 1),
            "threat_level_id": fields.get("threat_level_id", 1),
            "category_id": fields.get("category_id", 1),
            "geometry": fields.get("geometry", {
                "type": "Point",
                "coordinates": [30.3158, 59.9311]
            }),
            "registered_at": fields.get("registered_at", datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")),
            "resolve_rules": fields.get("resolve_rules", 1)
        }
        return requests.put(f"{self.base_url}/incident/{incident_id}", json=data, headers=self.headers, verify=False)
    
    def delete_incident(self, incident_id):
        """Удалить инцидент"""
        return requests.delete(f"{self.base_url}/incident/{incident_id}", headers=self.headers, verify=False)
    
    # === EVENTS ===
    def get_events_list(self):
        """Получить список событий"""
        return requests.get(f"{self.base_url}/event", headers=self.headers, verify=False)
    
    def get_event_by_id(self, event_id):
        """Получить событие по ID"""
        return requests.get(f"{self.base_url}/event/{event_id}", headers=self.headers, verify=False)
    
    def create_event(self, name, description, short_name=None):
        """Создать событие с полными данными"""
        from datetime import datetime, timedelta
        
        if not short_name:
            short_name = name[:20]  # Первые 20 символов как короткое имя
            
        now = datetime.now()
        data = {
            "name": name,
            "description": description,
            "short_name": short_name,
            "date_start": now.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "date_end": (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        }
        return requests.post(f"{self.base_url}/event", json=data, headers=self.headers, verify=False)
    
    def update_event(self, event_id, **fields):
        """Обновить событие с полными данными"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        data = {
            "name": fields.get("name", "Обновленное событие"),
            "description": fields.get("description", "Обновленное описание"),
            "short_name": fields.get("short_name", "Обновленное"),
            "date_start": fields.get("date_start", now.strftime("%Y-%m-%dT%H:%M:%S+00:00")),
            "date_end": fields.get("date_end", (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00"))
        }
        return requests.put(f"{self.base_url}/event/{event_id}", json=data, headers=self.headers, verify=False)
    
    def delete_event(self, event_id):
        """Удалить событие"""
        return requests.delete(f"{self.base_url}/event/{event_id}", headers=self.headers, verify=False)
    
    # === CATEGORIES ===
    def get_categories_list(self):
        """Получить список категорий"""
        return requests.get(f"{self.base_url}/category", headers=self.headers, verify=False)
    
    def get_category_by_id(self, category_id):
        """Получить категорию по ID"""
        return requests.get(f"{self.base_url}/category/{category_id}", headers=self.headers, verify=False)
    
    def create_category(self, name, description):
        """Создать категорию"""
        data = {"name": name, "description": description}
        return requests.post(f"{self.base_url}/category", json=data, headers=self.headers, verify=False)
    
    def update_category(self, category_id, **fields):
        """Обновить категорию"""
        return requests.put(f"{self.base_url}/category/{category_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_category(self, category_id):
        """Удалить категорию"""
        return requests.delete(f"{self.base_url}/category/{category_id}", headers=self.headers, verify=False)
    
    # === KEYWORDS ===
    def get_keywords_list(self):
        """Получить список ключевых слов"""
        return requests.get(f"{self.base_url}/keyword", headers=self.headers, verify=False)
    
    def get_keyword_by_id(self, keyword_id):
        """Получить ключевое слово по ID"""
        return requests.get(f"{self.base_url}/keyword/{keyword_id}", headers=self.headers, verify=False)
    
    def create_keyword(self, name, description):
        """Создать ключевое слово"""
        data = {"name": name, "description": description}
        return requests.post(f"{self.base_url}/keyword", json=data, headers=self.headers, verify=False)
    
    def update_keyword(self, keyword_id, **fields):
        """Обновить ключевое слово"""
        return requests.put(f"{self.base_url}/keyword/{keyword_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_keyword(self, keyword_id):
        """Удалить ключевое слово"""
        return requests.delete(f"{self.base_url}/keyword/{keyword_id}", headers=self.headers, verify=False)
    
    # === FACTORS ===
    def get_factors_list(self, page=1, limit=25, name=None):
        """Получить список факторов"""
        params = {"page": page, "limit": limit}
        if name:
            params["name"] = name
        return requests.get(f"{self.base_url}/factor", params=params, headers=self.headers, verify=False)
    
    def get_factor_by_id(self, factor_id):
        """Получить фактор по ID"""
        return requests.get(f"{self.base_url}/factor/{factor_id}", headers=self.headers, verify=False)
    
    def create_factor(self, name, is_geo=False):
        """Создать фактор"""
        data = {"name": name, "is_geo": is_geo}
        return requests.post(f"{self.base_url}/factor", json=data, headers=self.headers, verify=False)
    
    def update_factor(self, factor_id, **fields):
        """Обновить фактор с полными данными"""
        data = {
            "name": fields.get("name", "Обновленный фактор"),
            "is_geo": fields.get("is_geo", False)
        }
        return requests.put(f"{self.base_url}/factor/{factor_id}", json=data, headers=self.headers, verify=False)
    
    def delete_factor(self, factor_id):
        """Удалить фактор"""
        return requests.delete(f"{self.base_url}/factor/{factor_id}", headers=self.headers, verify=False)
