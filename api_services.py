#!/usr/bin/env python3
"""
Простой сервисный слой
"""

from api_client_incidents import SimpleAPIClient


class SimpleAPIService:
    """Универсальный сервис для работы с API"""
    
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
    
    def create_incident(self, name, description, type_id=1, status_id=1, threat_level_id=1, category_id=1):
        """Создать новый инцидент"""
        response = self.client.create_incident(name, description, type_id, status_id, threat_level_id, category_id)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Creation error: {response.status_code} - {response.text}")
    
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
    
    # === EVENTS ===
    def get_all_events(self):
        """Получить все события"""
        response = self.client.get_events_list()
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения списка событий: {response.status_code}")
    
    def get_event_by_id(self, event_id):
        """Получить событие по ID"""
        response = self.client.get_event_by_id(event_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения события: {response.status_code}")
    
    def create_event(self, name, description, short_name=None):
        """Создать новое событие"""
        response = self.client.create_event(name, description, short_name)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Event creation error: {response.status_code} - {response.text}")
    
    def update_event(self, event_id, **fields):
        """Обновить событие"""
        response = self.client.update_event(event_id, **fields)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка обновления события: {response.status_code}")
    
    def delete_event(self, event_id):
        """Удалить событие"""
        response = self.client.delete_event(event_id)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Ошибка удаления события: {response.status_code}")
    
    # === CATEGORIES ===
    def get_all_categories(self):
        """Получить все категории"""
        response = self.client.get_categories_list()
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения списка категорий: {response.status_code}")
    
    def get_category_by_id(self, category_id):
        """Получить категорию по ID"""
        response = self.client.get_category_by_id(category_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения категории: {response.status_code}")
    
    def create_category(self, name, description):
        """Создать новую категорию"""
        response = self.client.create_category(name, description)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка создания категории: {response.status_code}")
    
    def update_category(self, category_id, **fields):
        """Обновить категорию"""
        response = self.client.update_category(category_id, **fields)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка обновления категории: {response.status_code}")
    
    def delete_category(self, category_id):
        """Удалить категорию"""
        response = self.client.delete_category(category_id)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Ошибка удаления категории: {response.status_code}")
    
    # === KEYWORDS ===
    def get_all_keywords(self):
        """Получить все ключевые слова"""
        response = self.client.get_keywords_list()
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения списка ключевых слов: {response.status_code}")
    
    def get_keyword_by_id(self, keyword_id):
        """Получить ключевое слово по ID"""
        response = self.client.get_keyword_by_id(keyword_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения ключевого слова: {response.status_code}")
    
    def create_keyword(self, name, description):
        """Создать новое ключевое слово"""
        response = self.client.create_keyword(name, description)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка создания ключевого слова: {response.status_code}")
    
    def update_keyword(self, keyword_id, **fields):
        """Обновить ключевое слово"""
        response = self.client.update_keyword(keyword_id, **fields)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка обновления ключевого слова: {response.status_code}")
    
    def delete_keyword(self, keyword_id):
        """Удалить ключевое слово"""
        response = self.client.delete_keyword(keyword_id)
        if response.status_code in [200, 204]:
            return True
        else:
            raise Exception(f"Ошибка удаления ключевого слова: {response.status_code}")
    
    # === FACTORS ===
    def get_all_factors(self, page=1, limit=25, name=None):
        """Получить все факторы"""
        response = self.client.get_factors_list(page, limit, name)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения списка факторов: {response.status_code}")
    
    def get_factor_by_id(self, factor_id):
        """Получить фактор по ID"""
        response = self.client.get_factor_by_id(factor_id)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения фактора: {response.status_code}")
    
    def create_factor(self, name, is_geo=False):
        """Создать новый фактор"""
        response = self.client.create_factor(name, is_geo)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка создания фактора: {response.status_code}")
    
    def update_factor(self, factor_id, **fields):
        """Обновить фактор"""
        response = self.client.update_factor(factor_id, **fields)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            raise Exception(f"Ошибка обновления фактора: {response.status_code} - {response.text}")
    
    def delete_factor(self, factor_id):
        """Удалить фактор"""
        response = self.client.delete_factor(factor_id)
        if response.status_code in [200, 204]:
            return True
        elif response.status_code == 422 and "is_system" in response.text:
            raise Exception("Системный фактор нельзя удалять - это нормально")
        else:
            raise Exception(f"Ошибка удаления фактора: {response.status_code}")
    
    def search_factors(self, name):
        """Поиск факторов по имени"""
        return self.get_all_factors(name=name)


# Для обратной совместимости
SimpleIncidentService = SimpleAPIService
