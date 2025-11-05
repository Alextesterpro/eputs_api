#!/usr/bin/env python3
"""
API клиент для Organizations (Организации)
"""

import requests
from typing import Dict, Any, Optional, List
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OrganizationsAPIClient:
    """API клиент для работы с Организациями"""
    
    def __init__(self):
        self.base_url = "http://91.227.17.139/services/organization"
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
            response = self.organization_list(page=1, limit=1)
            return response.status_code == 200
        except Exception:
            return False
    
    # ===== Organizations =====
    
    def organization_list(self, page: int = 1, limit: int = 25) -> requests.Response:
        """Получение списка организаций"""
        url = f"{self.base_url}/api/organization"
        params = {"page": page, "limit": limit}
        return requests.get(url, params=params, headers=self.headers, verify=False, timeout=30)
    
    def organization_create(self, title: str, full_name: str, inn: str,
                           juristic_address: Dict[str, str],
                           mail_address: Dict[str, str],
                           real_address: Dict[str, str],
                           phones: List[Dict[str, str]] = None,
                           emails: List[str] = None) -> requests.Response:
        """Создание организации"""
        url = f"{self.base_url}/api/organization"
        payload = {
            "title": title,
            "full_name": full_name,
            "inn": inn,
            "juristic_address": juristic_address,
            "mail_address": mail_address,
            "real_address": real_address,
            "phones": phones or [],
            "emails": emails or []
        }
        return requests.post(url, json=payload, headers=self.headers, verify=False, timeout=30)
    
    def organization_update(self, org_id: int, **fields) -> requests.Response:
        """Обновление организации"""
        url = f"{self.base_url}/api/organization/{org_id}"
        return requests.put(url, json=fields, headers=self.headers, verify=False, timeout=30)
    
    def organization_delete(self, org_id: int) -> requests.Response:
        """Удаление организации"""
        url = f"{self.base_url}/api/organization/{org_id}"
        return requests.delete(url, headers=self.headers, verify=False, timeout=30)
    
    def organization_add_attachments(self, org_id: int, attachments: List[Dict[str, Any]]) -> requests.Response:
        """Добавление документов к организации"""
        url = f"{self.base_url}/api/organization/{org_id}"
        payload = {"attachments": attachments}
        return requests.put(url, json=payload, headers=self.headers, verify=False, timeout=30)
    
    # ===== Roles =====
    
    def role_list(self, page: int = 1, limit: int = 25) -> requests.Response:
        """Получение списка ролей организаций"""
        url = f"{self.base_url}/api/role/"
        params = {"page": page, "limit": limit}
        return requests.get(url, params=params, headers=self.headers, verify=False, timeout=30)
    
    def role_create(self, name: str) -> requests.Response:
        """Создание роли"""
        url = f"{self.base_url}/api/role"
        payload = {"name": name}
        return requests.post(url, json=payload, headers=self.headers, verify=False, timeout=30)
    
    def role_update(self, role_id: int, name: str) -> requests.Response:
        """Обновление роли"""
        url = f"{self.base_url}/api/role/{role_id}"
        payload = {"name": name}
        return requests.put(url, json=payload, headers=self.headers, verify=False, timeout=30)
    
    def role_delete(self, role_id: int) -> requests.Response:
        """Удаление роли"""
        url = f"{self.base_url}/api/role/{role_id}"
        return requests.delete(url, headers=self.headers, verify=False, timeout=30)
    
    # ===== Role Contracts =====
    
    def role_contracts_upload(self, role_contracts: List[Dict[str, Any]]) -> requests.Response:
        """Добавление роли и договора к организации"""
        url = f"{self.base_url}/api/role/contracts/upload"
        payload = {"role_contracts": role_contracts}
        return requests.post(url, json=payload, headers=self.headers, verify=False, timeout=30)
    
    def role_contracts_delete_by_organization(self, organization_id: int) -> requests.Response:
        """Удаление ролей и договоров по ID организации"""
        url = f"{self.base_url}/api/role/contracts/by_organization"
        params = {"organization_id": organization_id}
        return requests.delete(url, params=params, headers=self.headers, verify=False, timeout=30)

