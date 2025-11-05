#!/usr/bin/env python3
"""
API клиент для Data Bus (Общая шина)
"""

import requests
from typing import Dict, Any, Optional, List
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DataBusAPIClient:
    """API клиент для работы с Data Bus"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/data-bus"
        self.token = self._get_token()
        self.headers = self._get_headers()
    
    def _get_token(self) -> str:
        """Получает токен из .env файла"""
        token = None
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('EPUTS_TOKEN=') or line.startswith('API_TOKEN='):
                        token = line.split('=', 1)[1].strip()
                        break
        
        if not token:
            raise ValueError("Токен не найден! Запустите refresh_token.py")
        
        return token
    
    def _get_headers(self) -> Dict[str, str]:
        """Формирует заголовки запроса"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "project": "98_spb"
        }
    
    def check_token(self) -> bool:
        """Проверяет валидность токена"""
        try:
            response = self.collection_service_list()
            return response.status_code == 200
        except Exception:
            return False
    
    # ===== Collection Services =====
    
    def collection_service_list(self) -> requests.Response:
        """Получение списка сервисов сбора данных"""
        url = f"{self.base_url}/api/collection-service/list"
        return requests.post(url, json={}, headers=self.headers, verify=False)
    
    def collection_service_create(self, name: str, template: Dict[str, Any], 
                                   service_id: int, template_id: int) -> requests.Response:
        """Создание сервиса сбора данных"""
        url = f"{self.base_url}/api/collection-service"
        payload = {
            "name": name,
            "template": template,
            "service_id": service_id,
            "template_id": template_id
        }
        return requests.post(url, json=payload, headers=self.headers, verify=False)
    
    def collection_service_update(self, service_id: int, name: str, 
                                   template: Dict[str, Any], 
                                   service_type_id: int, template_id: int) -> requests.Response:
        """Обновление сервиса сбора данных"""
        url = f"{self.base_url}/api/collection-service/{service_id}"
        payload = {
            "name": name,
            "template": template,
            "service_id": service_type_id,
            "template_id": template_id
        }
        return requests.put(url, json=payload, headers=self.headers, verify=False)
    
    def collection_service_delete(self, service_id: int) -> requests.Response:
        """Удаление сервиса сбора данных"""
        url = f"{self.base_url}/api/collection-service/{service_id}"
        return requests.delete(url, headers=self.headers, verify=False)
    
    # ===== Jobs =====
    
    def job_list(self) -> requests.Response:
        """Получение списка задач"""
        url = f"{self.base_url}/api/job/list"
        return requests.post(url, json={}, headers=self.headers, verify=False)
    
    # ===== Relay Services =====
    
    def relay_service_list(self) -> requests.Response:
        """Получение списка сервисов ретрансляции"""
        url = f"{self.base_url}/api/relay-service/list"
        return requests.post(url, json={}, headers=self.headers, verify=False)
    
    # EGTS Clone
    
    def relay_egts_clone_create(self, name: str, ip: str, port: int, 
                                 collection_service_id_list: List[int],
                                 service_id: int = 1, template_id: int = 1) -> requests.Response:
        """Создание сервиса ретрансляции EGTS клон"""
        url = f"{self.base_url}/api/relay-service/egts-clone"
        payload = {
            "name": name,
            "template": {
                "ip": ip,
                "port": port,
                "collection_service_id_list": collection_service_id_list
            },
            "service_id": service_id,
            "template_id": template_id,
            "ip": ip,
            "port": port,
            "collection_service_id_list": collection_service_id_list
        }
        return requests.post(url, json=payload, headers=self.headers, verify=False)
    
    def relay_egts_clone_update(self, relay_id: int, name: str, ip: str, port: int,
                                 collection_service_id_list: List[int],
                                 service_id: int = 1, template_id: int = 1) -> requests.Response:
        """Обновление сервиса ретрансляции EGTS клон"""
        url = f"{self.base_url}/api/relay-service/egts-clone/{relay_id}"
        payload = {
            "name": name,
            "template": {
                "ip": ip,
                "port": port,
                "collection_service_id_list": collection_service_id_list
            },
            "service_id": service_id,
            "template_id": template_id,
            "ip": ip,
            "port": port,
            "collection_service_id_list": collection_service_id_list
        }
        return requests.put(url, json=payload, headers=self.headers, verify=False)
    
    def relay_egts_clone_delete(self, relay_id: int) -> requests.Response:
        """Удаление сервиса ретрансляции EGTS клон"""
        url = f"{self.base_url}/api/relay-service/egts-clone/{relay_id}"
        return requests.delete(url, headers=self.headers, verify=False)
    
    # EGTS Telemetry
    
    def relay_egts_telemetry_create(self, name: str, ip: str, port: int,
                                     type_id_list: List[int], organization_id_list: List[int],
                                     id_field: int, service_id: int = 3, 
                                     template_id: int = 6) -> requests.Response:
        """Создание сервиса ретрансляции EGTS телеметрия"""
        url = f"{self.base_url}/api/relay-service/egts-telemetry"
        payload = {
            "name": name,
            "template": {
                "ip": ip,
                "port": port,
                "type_id_list": type_id_list,
                "organization_id_list": organization_id_list,
                "id_field": {"id": id_field, "name": "OID" if id_field == 1 else "Other"}
            },
            "service_id": service_id,
            "template_id": template_id,
            "ip": ip,
            "port": port,
            "type_id_list": type_id_list,
            "organization_id_list": organization_id_list,
            "id_field": id_field
        }
        return requests.post(url, json=payload, headers=self.headers, verify=False)
    
    def relay_egts_telemetry_update(self, relay_id: int, name: str, ip: str, port: int,
                                     type_id_list: List[int], organization_id_list: List[int],
                                     id_field: int, service_id: int = 3,
                                     template_id: int = 6) -> requests.Response:
        """Обновление сервиса ретрансляции EGTS телеметрия"""
        url = f"{self.base_url}/api/relay-service/egts-telemetry/{relay_id}"
        payload = {
            "name": name,
            "template": {
                "ip": ip,
                "port": port,
                "type_id_list": type_id_list,
                "organization_id_list": organization_id_list,
                "id_field": {"id": id_field, "name": "OID" if id_field == 1 else "Other"}
            },
            "service_id": service_id,
            "template_id": template_id,
            "ip": ip,
            "port": port,
            "type_id_list": type_id_list,
            "organization_id_list": organization_id_list,
            "id_field": id_field
        }
        return requests.put(url, json=payload, headers=self.headers, verify=False)
    
    def relay_egts_telemetry_delete(self, relay_id: int) -> requests.Response:
        """Удаление сервиса ретрансляции EGTS телеметрия"""
        url = f"{self.base_url}/api/relay-service/egts-telemetry/{relay_id}"
        return requests.delete(url, headers=self.headers, verify=False)

