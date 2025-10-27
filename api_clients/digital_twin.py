#!/usr/bin/env python3
"""
API клиент для раздела Цифровой двойник
Включает: дорожную сеть, инфраструктуру, граф УДС
"""

import requests
import os


class DigitalTwinAPIClient:
    """API клиент для Цифрового двойника"""
    
    def __init__(self):
        self.road_network_url = "http://91.227.17.139/services/road-network/api"
        self.cifdv_graph_url = "http://91.227.17.139/services/cifdv-graph/api"
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
                f"{self.road_network_url}/infrastructure",
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
    
    # === Инфраструктура ===
    
    def get_infrastructure_list(self, page=1, limit=25):
        """Получить список объектов инфраструктуры"""
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.road_network_url}/infrastructure", params=params, headers=self.headers, verify=False)
    
    def get_infrastructure_by_polygon(self, polygon_data):
        """Получить объекты инфраструктуры по полигону"""
        return requests.post(f"{self.road_network_url}/infrastructure/polygon", json=polygon_data, headers=self.headers, verify=False)
    
    def create_infrastructure(self, name, description, lat, lon, type_id, organization_id, address, address_text, geometry):
        """Создать объект инфраструктуры"""
        data = {
            "name": name,
            "description": description,
            "lat": lat,
            "lon": lon,
            "type_id": type_id,
            "organization_id": organization_id,
            "address": address,
            "address_text": address_text,
            "geometry": geometry
        }
        return requests.post(f"{self.road_network_url}/infrastructure", json=data, headers=self.headers, verify=False)
    
    def update_infrastructure(self, infrastructure_id, **fields):
        """Обновить объект инфраструктуры"""
        return requests.put(f"{self.road_network_url}/infrastructure/{infrastructure_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_infrastructure(self, infrastructure_id):
        """Удалить объект инфраструктуры"""
        return requests.delete(f"{self.road_network_url}/infrastructure/{infrastructure_id}", headers=self.headers, verify=False)
    
    # === Типы инфраструктуры ===
    
    def get_infrastructure_types_list(self, page=1, limit=25):
        """Получить список типов объектов инфраструктуры"""
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.road_network_url}/infrastructure_type", params=params, headers=self.headers, verify=False)
    
    def create_infrastructure_type(self, name):
        """Создать тип объекта инфраструктуры"""
        data = {"name": name}
        return requests.post(f"{self.road_network_url}/infrastructure_type/", json=data, headers=self.headers, verify=False)
    
    def update_infrastructure_type(self, type_id, name):
        """Обновить тип объекта инфраструктуры"""
        data = {"name": name}
        return requests.put(f"{self.road_network_url}/infrastructure_type/{type_id}", json=data, headers=self.headers, verify=False)
    
    def delete_infrastructure_type(self, type_id):
        """Удалить тип объекта инфраструктуры"""
        return requests.delete(f"{self.road_network_url}/infrastructure_type/{type_id}", headers=self.headers, verify=False)
    
    # === Элементы дорожной сети ===
    
    def get_road_sections_list(self, page=1, limit=25):
        """Получить список элементов дорожной сети"""
        params = {"page": page, "limit": limit}
        return requests.get(f"{self.road_network_url}/road-section", params=params, headers=self.headers, verify=False)
    
    def get_road_sections_by_polygon(self, polygon_data):
        """Получить элементы дорожной сети по полигону"""
        return requests.post(f"{self.road_network_url}/road-section/polygon", json=polygon_data, headers=self.headers, verify=False)
    
    def create_road_section(self, name, description, address_text, fixated_at, category, type_val, status, length, lat, lon, organization_id, cadastre, address, geometry, data):
        """Создать элемент дорожной сети"""
        payload = {
            "name": name,
            "description": description,
            "address_text": address_text,
            "fixated_at": fixated_at,
            "category": category,
            "type": type_val,
            "status": status,
            "length": length,
            "lat": lat,
            "lon": lon,
            "organization_id": organization_id,
            "cadastre": cadastre,
            "address": address,
            "geometry": geometry,
            "data": data,
            "created_at": None
        }
        return requests.post(f"{self.road_network_url}/road-section", json=payload, headers=self.headers, verify=False)
    
    def update_road_section(self, section_id, **fields):
        """Обновить элемент дорожной сети"""
        return requests.put(f"{self.road_network_url}/road-section/{section_id}", json=fields, headers=self.headers, verify=False)
    
    def delete_road_section(self, section_id):
        """Удалить элемент дорожной сети"""
        return requests.delete(f"{self.road_network_url}/road-section/{section_id}", headers=self.headers, verify=False)
    
    def get_road_section_report(self, report_format="XLS"):
        """Получить отчет по элементам дорожной сети"""
        params = {"report": 1, "formats[]": report_format}
        return requests.get(f"{self.road_network_url}/road-section", params=params, headers=self.headers, verify=False)
    
    # === Граф УДС ===
    
    def get_graph(self, geometry, zoom=9):
        """Получить граф УДС по полигону"""
        data = {"geometry": geometry, "zoom": zoom}
        return requests.post(f"{self.cifdv_graph_url}/v2/get-graph", json=data, headers=self.headers, verify=False)
    
    # === Ревизии ===
    
    def get_revisions_list(self, page=1, per_page=25, sorting="created_at"):
        """Получить список ревизий"""
        params = {"page": page, "per_page": per_page, "sorting": sorting}
        return requests.get(f"{self.cifdv_graph_url}/v2/revisions", params=params, headers=self.headers, verify=False)
    
    # === Узлы ===
    
    def get_nodes_list(self, page=1, per_page=25):
        """Получить список узлов"""
        params = {"page": page, "per_page": per_page}
        return requests.get(f"{self.cifdv_graph_url}/nodes", params=params, headers=self.headers, verify=False)
    
    def create_node(self, lat, lon, geometry, node_type="Point"):
        """Создать узел"""
        data = {
            "lat": str(lat),
            "lon": str(lon),
            "geometry": geometry,
            "type": node_type
        }
        return requests.post(f"{self.cifdv_graph_url}/nodes", json=data, headers=self.headers, verify=False)
    
    def delete_node(self, node_id):
        """Удалить узел"""
        return requests.delete(f"{self.cifdv_graph_url}/nodes/{node_id}", headers=self.headers, verify=False)
    
    # === Атрибуты ===
    
    def get_attributes_list(self, page=1, per_page=25):
        """Получить список атрибутов"""
        params = {"page": page, "per_page": per_page}
        return requests.get(f"{self.cifdv_graph_url}/v2/attributes", params=params, headers=self.headers, verify=False)
    
    # === Вспомогательные методы ===
    
    @staticmethod
    def generate_test_polygon():
        """Генерировать тестовый полигон"""
        return {
            "polygon": {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[28.731994628906254, 60.105932794980426], [31.893310546875004, 60.105932794980426], [31.893310546875004, 59.77160889270327], [28.731994628906254, 59.77160889270327], [28.731994628906254, 60.105932794980426]]]
                }
            }
        }
    
    @staticmethod
    def generate_test_geometry(lon, lat):
        """Генерировать тестовую геометрию точки"""
        return {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            }
        }

